# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

from __future__ import annotations

import logging

import bpy
import MaterialX as mx

from . import lib
from . import material_flatten as mf
from . import material_properties as mp
from . import materialx_handle as mh

logger = logging.getLogger(__name__)


def generate_material(material: mp.Material):
    handle = mh.get_material_handler(material)
    doc: mx.Document = handle.document

    if not doc:
        return

    doc = doc.copy()
    try:
        doc = mf.flatten(doc)
    except Exception as e:
        logger.warning("Failed to flatten MaterialX document: %s", e)
        return

    node_group_name = f"MaterialX_{material.name}"
    node_group: bpy.types.NodeTree = bpy.data.node_groups.get(node_group_name)
    if node_group is None:
        node_group = bpy.data.node_groups.new(
            node_group_name, bpy.types.ShaderNodeTree.__name__
        )

    node_group.nodes.clear()

    static_types = ("filename", "string")

    node_mapping = {}
    for node in doc.getNodes():
        node: mx.Node
        node_def = node.getNodeDef().getName()
        blender_node_type = lib.node_registry.materialx_nodes.get(node_def)
        if blender_node_type is None:
            logger.warning(
                "No mapping found for node %s with NodeDef %s. Skipping.",
                node.getName(),
                node_def,
            )
            continue
        node_mapping[node.getName()] = blender_node_type(node_group, node)
    for node in doc.getNodes():
        node: mx.Node
        if node.getName() not in node_mapping:
            logger.warning(
                "Node %s not found in node mapping. Skipping.", node.getName()
            )
            continue
        _, inputs, outputs = node_mapping[node.getName()]
        for _input in node.getInputs():
            _input: mx.Input
            if _input.getType() in static_types:
                # avoid always warning for image texture file inputs
                continue
            if _input.getName() not in inputs:
                logger.warning(
                    "Input %s of node %s not found in inputs. Skipping.",
                    _input.getName(),
                    node.getName(),
                )
                continue
            connected_node = None
            connected_output_name = "out"
            if _input.getConnectedOutput():
                connected_output: mx.Output = _input.getConnectedOutput()
                connected_node = doc.getNode(connected_output.getNodeName())
                connected_output_name = connected_output.getName()
            elif _input.getConnectedNode():
                connected_node: mx.Node = _input.getConnectedNode()
                if connected_node.getOutputs():
                    connected_output_name = connected_node.getOutputs()[
                        0
                    ].getName()
            if not connected_node:
                continue
            if connected_node.getName() not in node_mapping:
                logger.warning(
                    "Node %s not found in node mapping. Skipping.",
                    connected_node.getName(),
                )
                continue
            _, _, outputs = node_mapping.get(connected_node.getName())
            if connected_output_name not in outputs:
                logger.warning(
                    "Output %s of node %s not found in outputs. Skipping.",
                    connected_output_name,
                    connected_node.getName(),
                )
                continue
            blender_node_input = inputs[_input.getName()]
            blender_node_output = outputs[connected_output_name]
            node_group.links.new(blender_node_input, blender_node_output)

    material.use_nodes = True

    material_tree = material.node_tree
    material_tree.nodes.clear()
    group_node: bpy.types.ShaderNodeGroup = material_tree.nodes.new(
        bpy.types.ShaderNodeGroup.__name__
    )
    group_node.node_tree = node_group
