# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import logging

import bpy
import MaterialX as mx

logger = logging.getLogger(__name__)


def node_declaration_get_default_values(mx_node: mx.Node):
    default_values = {}
    declaration: mx.InterfaceElement = mx_node.getDeclaration()
    if declaration.getInheritsFrom():
        default_values = node_declaration_get_default_values(
            declaration.getInheritsFrom()
        )
    for _input in declaration.getInputs():
        _input: mx.Input
        value = _input._getValue()
        if value is None:
            continue
        default_values[_input.getName()] = value
    return default_values


def node_get_default_values(mx_node: mx.Node):
    default_values = node_declaration_get_default_values(mx_node)
    for _input in mx_node.getInputs():
        _input: mx.Input
        value = _input._getValue()
        if value is None:
            continue
        default_values[_input.getName()] = value
    return default_values


def cast_value_to_socket_type(value: mx.Value, socket_type: str):
    data = value.getData()
    if isinstance(data, mx.Vector3) and socket_type == "VECTOR":
        return data.asTuple()
    if isinstance(data, mx.Vector2) and socket_type == "VECTOR":
        return tuple([data.asTuple()[0], data.asTuple()[1], 1.0])
    elif isinstance(data, mx.Vector4) and socket_type == "BUNDLE":
        raise NotImplementedError(
            "Vector4 to Bundle conversion not implemented yet"
        )
    elif isinstance(data, mx.Color3) and socket_type == "RGBA":
        return list(data.asTuple()) + [1.0]
    elif isinstance(data, mx.Color4) and socket_type == "RGBA":
        return data.asTuple()
    elif isinstance(data, bool) and socket_type == "VALUE":
        return 1.0 if data else 0.0
    return data


def apply_default_values(
    mx_node: mx.Node, blender_inputs: dict[str, bpy.types.NodeSocket]
):
    default_values = node_get_default_values(mx_node)
    for key, value in default_values.items():
        if key not in blender_inputs:
            continue
        blender_input = blender_inputs[key]
        if not isinstance(blender_input, bpy.types.NodeSocket):
            continue
        try:
            if blender_input.type == "BUNDLE":
                logger.info(
                    "Cannot set default value for bundle socket: %s", key
                )
                # TODO: Support default values for bundles (e.g. spawn a combine node and set its values)
                continue
            blender_input.default_value = cast_value_to_socket_type(
                value, blender_input.type
            )
        except Exception as e:
            logger.error("Error setting default value for %s: %s", key, e)
            pass


def create_blender_node(
    tree: bpy.types.NodeTree, mx_node: mx.Node, node_type: type[bpy.types.Node]
):
    try:
        xpos = float(mx_node.getAttribute("xpos")) * 250.0
        ypos = float(mx_node.getAttribute("ypos")) * 250.0
    except:
        xpos = 0.0
        ypos = 0.0
    if isinstance(node_type, str):
        node = tree.nodes.new(node_type)
    else:
        node = tree.nodes.new(node_type.__name__)
    node.name = mx_node.getName()
    node.label = mx_node.getName()
    node.location = (xpos, ypos)
    return node


def blender_to_vector4_bundle(
    tree: bpy.types.NodeTree, mx_node: mx.Node, node_type: type[bpy.types.Node]
):
    bundle = create_blender_node(tree, mx_node, bpy.types.NodeCombineBundle)
    bundle.bundle_items.new("FLOAT", "X")
    bundle.bundle_items.new("FLOAT", "Y")
    bundle.bundle_items.new("FLOAT", "Z")
    bundle.bundle_items.new("FLOAT", "W")
    bundle.define_signature = True
    bundle.inputs[0].default_value = 0.0
    bundle.inputs[1].default_value = 0.0
    bundle.inputs[2].default_value = 0.0
    bundle.inputs[3].default_value = 0.0
    return bundle


def blender_from_vector4_bundle(
    tree: bpy.types.NodeTree, mx_node: mx.Node, node_type: type[bpy.types.Node]
):
    bundle = create_blender_node(tree, mx_node, bpy.types.NodeSeparateBundle)
    bundle.bundle_items.new("FLOAT", "X")
    bundle.bundle_items.new("FLOAT", "Y")
    bundle.bundle_items.new("FLOAT", "Z")
    bundle.bundle_items.new("FLOAT", "W")
    bundle.define_signature = True
    return bundle


def blender_to_color4_bundle(
    tree: bpy.types.NodeTree, mx_node: mx.Node, node_type: type[bpy.types.Node]
):
    bundle = create_blender_node(tree, mx_node, bpy.types.NodeCombineBundle)
    bundle.bundle_items.new("FLOAT", "R")
    bundle.bundle_items.new("FLOAT", "G")
    bundle.bundle_items.new("FLOAT", "B")
    bundle.bundle_items.new("FLOAT", "A")
    bundle.define_signature = True
    bundle.inputs[0].default_value = 0.0
    bundle.inputs[1].default_value = 0.0
    bundle.inputs[2].default_value = 0.0
    bundle.inputs[3].default_value = 0.0
    return bundle


def blender_from_color4_bundle(
    tree: bpy.types.NodeTree, mx_node: mx.Node, node_type: type[bpy.types.Node]
):
    bundle = create_blender_node(tree, mx_node, bpy.types.NodeSeparateBundle)
    bundle.bundle_items.new("FLOAT", "R")
    bundle.bundle_items.new("FLOAT", "G")
    bundle.bundle_items.new("FLOAT", "B")
    bundle.bundle_items.new("FLOAT", "A")
    bundle.define_signature = True
    return bundle
