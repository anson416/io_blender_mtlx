# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

from __future__ import annotations

import logging
import os

import MaterialX as mx

from . import lib

logger = logging.getLogger(__name__)


def flatten_nodegraph(
    doc: mx.Document, nodegraph: mx.NodeGraph
) -> list[mx.NodeGraph]:
    existing_nodes: list[mx.Node] = doc.getNodes() + doc.getNodeGraphs()

    mapping: dict[str, tuple[mx.Node, mx.Node]] = {}
    for node in nodegraph.getNodes():
        new_name = doc.createValidChildName(
            f"{nodegraph.getName()}_{node.getName()}"
        )
        new_node = doc.addNode(node.getCategory(), new_name, node.getType())
        new_node.copyContentFrom(node)
        mapping[node.getName()] = (node, new_node)

    for name, (node, new_node) in mapping.items():
        for _input in node.getInputs():
            if _input.getConnectedNode():
                # internal connection to another node in the new nodes
                connected_node_name = _input.getNodeName()
                new_node_input = new_node.getInput(_input.getName())
                connected_node_new = mapping[connected_node_name][1]
                new_node_input.setConnectedNode(connected_node_new)
            elif _input.getConnectedOutput():
                # internal connection to an output of another node in the new nodes
                connected_output: mx.Output = _input.getConnectedOutput()
                connected_node_name = connected_output.getNodeName()
                connected_node_new = mapping[connected_node_name][1]
                new_node_output = connected_node_new.getOutput(
                    connected_output.getName()
                )
                new_node.setConnectedOutput(
                    connected_node_new.getName(), new_node_output
                )
            elif _input.getInterfaceName():
                # internal connection to an input of the nodegraph
                connected_input = _input.getInterfaceName()
                outside_input = nodegraph.getInput(connected_input)
                new_node_input = new_node.getInput(_input.getName())
                new_node_input.copyContentFrom(outside_input)
                # the type for filename inputs is not copied correctly
                if (
                    _input.getType() == "filename"
                    and new_node_input.getType() == "string"
                ):
                    new_node_input.setType(_input.getType())

    for node in existing_nodes:
        for _input in node.getInputs():
            if not _input.getNodeGraphString() == nodegraph.getName():
                continue
            if (
                not _input.getConnectedNode()
                and not _input.getConnectedOutput()
            ):
                continue
            # the nodegraph is transparent and we have a connection to another node
            if _input.getConnectedNode():
                connected_node: mx.Node = _input.getConnectedNode()
                _input.setConnectedNode(mapping[connected_node.getName()][1])
                continue
            if _input.getConnectedOutput():
                connected_output: mx.Output = _input.getConnectedOutput()
                connected_node_name = connected_output.getNodeName()
                connected_node_new = mapping[connected_node_name][1]
                new_node_output = connected_node_new.getOutput(
                    connected_output.getName()
                )
                _input.setConnectedOutput(
                    mapping[connected_node_name][1], new_node_output
                )

    doc.removeNodeGraph(nodegraph.getName())


def has_blender_nodedef(node: mx.Node) -> bool:
    node_def = node.getNodeDef().getName()
    if node_def in lib.node_registry.materialx_nodes:
        # We have a known Blender implementation for this node type
        return False
    return True


def flatten(doc: mx.Document) -> mx.Document:
    nodegraphs = doc.getNodeGraphs()
    while nodegraphs:
        nodegraph = nodegraphs[0]
        flatten_nodegraph(doc, nodegraph)
        nodegraphs.pop(0)
        # TODO: handle nested nodegraphs

    mx.loadLibraries(
        mx.getDefaultDataLibraryFolders(), mx.getDefaultDataSearchPath(), doc
    )
    doc.flattenSubgraphs(filter=has_blender_nodedef)

    for node in doc.getNodes():
        for _input in node.getInputs():
            if _input.getType() != "filename":
                continue
            path = _input.getValueString()
            if not path:
                continue
            if os.path.isabs(path):
                continue

            abs_path = os.path.normpath(
                os.path.join(
                    os.path.dirname(doc.getSourceUri()),
                    doc.getFilePrefix(),
                    path,
                )
            )
            _input.setValueString(abs_path)

    return doc
