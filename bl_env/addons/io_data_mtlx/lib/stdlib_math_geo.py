# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import bpy
import MaterialX as mx

from .graph_utils import (
    apply_default_values,
    create_blender_node,
)
from .node_registry import register_materialx_node


# =============================================================================
# Factory helpers
# =============================================================================

def make_math_node(tree: bpy.types.NodeTree, mx_node: mx.Node, operation: str):
    """Binary float math: ShaderNodeMath with given operation."""
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMath)
    node.operation = operation
    node.update()
    mx_inputs = {"in1": node.inputs[0], "in2": node.inputs[1]}
    apply_default_values(mx_node, mx_inputs)
    return (node,), mx_inputs, {"out": node.outputs[0]}


def make_unary_math_node(tree: bpy.types.NodeTree, mx_node: mx.Node, operation: str):
    """Unary float math: ShaderNodeMath with given operation."""
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMath)
    node.operation = operation
    node.update()
    mx_inputs = {"in": node.inputs[0]}
    apply_default_values(mx_node, mx_inputs)
    return (node,), mx_inputs, {"out": node.outputs[0]}


def make_vector_math_node(tree: bpy.types.NodeTree, mx_node: mx.Node, operation: str):
    """Binary vector3 math: ShaderNodeVectorMath with given operation."""
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    node.operation = operation
    node.update()
    mx_inputs = {"in1": node.inputs[0], "in2": node.inputs[1]}
    apply_default_values(mx_node, mx_inputs)
    return (node,), mx_inputs, {"out": node.outputs[0]}


def make_color3_math(
    tree: bpy.types.NodeTree,
    mx_node: mx.Node,
    operations: list[str],
    op_type: str = "math",
):
    """
    Color3 math using SeparateColor -> per-channel Math -> CombineColor.
    operations: list of 3 operation strings for R, G, B channels.
    op_type: "math" for ShaderNodeMath, "clamp" is handled via CLAMP operation.
    """
    separate_node = create_blender_node(
        tree, mx_node, bpy.types.ShaderNodeSeparateColor
    )
    nodes = [separate_node]

    math_nodes = []
    for i, op in enumerate(operations):
        m = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMath)
        m.operation = op
        m.inputs[0].default_value = 0.0
        m.inputs[1].default_value = 0.0
        m.update()
        math_nodes.append(m)
        nodes.append(m)

    combine_node = create_blender_node(
        tree, mx_node, bpy.types.ShaderNodeCombineColor
    )
    nodes.append(combine_node)

    # Wire: separate -> math[i] -> combine[i]
    for i, m in enumerate(math_nodes):
        tree.links.new(m.inputs[0], separate_node.outputs[i])
        tree.links.new(combine_node.inputs[i], m.outputs[0])

    mx_inputs = {"in1": separate_node.inputs[0]}
    mx_inputs["in2"] = math_nodes[0].inputs[1]

    apply_default_values(mx_node, mx_inputs)

    return tuple(nodes), mx_inputs, {"out": combine_node.outputs[0]}


# =============================================================================
# Float math (binary)
# =============================================================================

@register_materialx_node("ND_add_float")
def ND_add_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_math_node(tree, mx_node, "ADD")


@register_materialx_node("ND_subtract_float")
def ND_subtract_float_new(tree: bpy.types.NodeTree, mx_node: mx.Node):
    # Renamed to avoid collision with potential imports; decorator registers this correctly.
    return make_math_node(tree, mx_node, "SUBTRACT")


@register_materialx_node("ND_divide_float")
def ND_divide_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_math_node(tree, mx_node, "DIVIDE")


@register_materialx_node("ND_power_float")
def ND_power_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_math_node(tree, mx_node, "POWER")


@register_materialx_node("ND_min_float")
def ND_min_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_math_node(tree, mx_node, "MINIMUM")


@register_materialx_node("ND_max_float")
def ND_max_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_math_node(tree, mx_node, "MAXIMUM")


@register_materialx_node("ND_modulo_float")
def ND_modulo_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_math_node(tree, mx_node, "MODULO")


# =============================================================================
# Float math (unary)
# =============================================================================

@register_materialx_node("ND_sin_float")
def ND_sin_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_unary_math_node(tree, mx_node, "SINE")


@register_materialx_node("ND_cos_float")
def ND_cos_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_unary_math_node(tree, mx_node, "COSINE")


@register_materialx_node("ND_tan_float")
def ND_tan_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_unary_math_node(tree, mx_node, "TANGENT")


@register_materialx_node("ND_absval_float")
def ND_absval_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_unary_math_node(tree, mx_node, "ABSOLUTE")


@register_materialx_node("ND_floor_float")
def ND_floor_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_unary_math_node(tree, mx_node, "FLOOR")


@register_materialx_node("ND_ceil_float")
def ND_ceil_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_unary_math_node(tree, mx_node, "CEIL")


@register_materialx_node("ND_round_float")
def ND_round_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_unary_math_node(tree, mx_node, "ROUND")


@register_materialx_node("ND_sqrt_float")
def ND_sqrt_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_unary_math_node(tree, mx_node, "SQRT")


@register_materialx_node("ND_invert_float")
def ND_invert_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_unary_math_node(tree, mx_node, "INVERT")


# =============================================================================
# Float (special)
# =============================================================================

@register_materialx_node("ND_clamp_float")
def ND_clamp_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMapRange)
    node.clamp = True
    node.data_type = "FLOAT"
    node.update()

    mx_inputs = {
        "in": node.inputs["Value"],
        "low": node.inputs["From Min"],
        "high": node.inputs["From Max"],
    }

    apply_default_values(mx_node, mx_inputs)

    return (node,), mx_inputs, {"out": node.outputs["Result"]}


@register_materialx_node("ND_mix_float")
def ND_mix_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMix)
    node.data_type = "FLOAT"
    node.factor_mode = "UNIFORM"
    node.update()
    node.inputs["A"].default_value = 0.0
    node.inputs["B"].default_value = 0.0
    node.inputs["Factor"].default_value = 0.0

    mx_inputs = {
        "fg": node.inputs["A"],
        "bg": node.inputs["B"],
        "mix": node.inputs["Factor"],
    }
    apply_default_values(mx_node, mx_inputs)

    return (node,), mx_inputs, {"out": node.outputs["Result"]}


# =============================================================================
# Vector3 math (binary)
# =============================================================================

@register_materialx_node("ND_add_vector3")
def ND_add_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_vector_math_node(tree, mx_node, "ADD")


@register_materialx_node("ND_subtract_vector3")
def ND_subtract_vector3_new(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_vector_math_node(tree, mx_node, "SUBTRACT")


@register_materialx_node("ND_divide_vector3")
def ND_divide_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_vector_math_node(tree, mx_node, "DIVIDE")


@register_materialx_node("ND_multiply_vector3")
def ND_multiply_vector3_new(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_vector_math_node(tree, mx_node, "MULTIPLY")


@register_materialx_node("ND_min_vector3")
def ND_min_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_vector_math_node(tree, mx_node, "MINIMUM")


@register_materialx_node("ND_max_vector3")
def ND_max_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_vector_math_node(tree, mx_node, "MAXIMUM")


@register_materialx_node("ND_power_vector3")
def ND_power_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_vector_math_node(tree, mx_node, "POWER")


@register_materialx_node("ND_modulo_vector3")
def ND_modulo_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_vector_math_node(tree, mx_node, "MODULO")


# =============================================================================
# Vector3 special ops
# =============================================================================

@register_materialx_node("ND_dotproduct_vector3")
def ND_dotproduct_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    node.operation = "DOT_PRODUCT"
    node.update()
    mx_inputs = {"in1": node.inputs[0], "in2": node.inputs[1]}
    apply_default_values(mx_node, mx_inputs)
    # DOT_PRODUCT output is scalar, on outputs[1] for VectorMath
    return (node,), mx_inputs, {"out": node.outputs[1]}


@register_materialx_node("ND_crossproduct_vector3")
def ND_crossproduct_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    node.operation = "CROSS_PRODUCT"
    node.update()
    mx_inputs = {"in1": node.inputs[0], "in2": node.inputs[1]}
    apply_default_values(mx_node, mx_inputs)
    return (node,), mx_inputs, {"out": node.outputs[0]}


@register_materialx_node("ND_normalize_vector3")
def ND_normalize_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    node.operation = "NORMALIZE"
    node.update()
    mx_inputs = {"in": node.inputs[0]}
    apply_default_values(mx_node, mx_inputs)
    return (node,), mx_inputs, {"out": node.outputs[0]}


@register_materialx_node("ND_magnitude_vector3")
def ND_magnitude_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    node.operation = "LENGTH"
    node.update()
    mx_inputs = {"in": node.inputs[0]}
    apply_default_values(mx_node, mx_inputs)
    return (node,), mx_inputs, {"out": node.outputs[1]}


# =============================================================================
# Color3 math (separate/apply/combine pattern)
# =============================================================================

@register_materialx_node("ND_add_color3")
def ND_add_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["ADD", "ADD", "ADD"])


@register_materialx_node("ND_subtract_color3")
def ND_subtract_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["SUBTRACT", "SUBTRACT", "SUBTRACT"])


@register_materialx_node("ND_divide_color3")
def ND_divide_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["DIVIDE", "DIVIDE", "DIVIDE"])


@register_materialx_node("ND_power_color3")
def ND_power_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["POWER", "POWER", "POWER"])


@register_materialx_node("ND_min_color3")
def ND_min_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["MINIMUM", "MINIMUM", "MINIMUM"])


@register_materialx_node("ND_max_color3")
def ND_max_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["MAXIMUM", "MAXIMUM", "MAXIMUM"])


@register_materialx_node("ND_sqrt_color3")
def ND_sqrt_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["SQRT", "SQRT", "SQRT"])


@register_materialx_node("ND_invert_color3")
def ND_invert_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["INVERT", "INVERT", "INVERT"])


@register_materialx_node("ND_absval_color3")
def ND_absval_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["ABSOLUTE", "ABSOLUTE", "ABSOLUTE"])


@register_materialx_node("ND_floor_color3")
def ND_floor_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["FLOOR", "FLOOR", "FLOOR"])


@register_materialx_node("ND_ceil_color3")
def ND_ceil_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["CEIL", "CEIL", "CEIL"])


@register_materialx_node("ND_round_color3")
def ND_round_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["ROUND", "ROUND", "ROUND"])


@register_materialx_node("ND_modulo_color3")
def ND_modulo_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["MODULO", "MODULO", "MODULO"])


@register_materialx_node("ND_clamp_color3")
def ND_clamp_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    return make_color3_math(tree, mx_node, ["CLAMP", "CLAMP", "CLAMP"])


# =============================================================================
# Geometric nodes
# =============================================================================

@register_materialx_node("ND_position_vector3")
def ND_position_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeNewGeometry)
    mx_inputs = {}
    return (node,), mx_inputs, {"out": node.outputs[0]}


@register_materialx_node("ND_normal_vector3")
def ND_normal_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeNewGeometry)
    mx_inputs = {}
    return (node,), mx_inputs, {"out": node.outputs[1]}


@register_materialx_node("ND_tangent_vector3")
def ND_tangent_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeNewGeometry)
    mx_inputs = {}
    return (node,), mx_inputs, {"out": node.outputs[2]}


# =============================================================================
# Procedural / noise nodes
# =============================================================================

@register_materialx_node("ND_fractal3d_float")
def ND_fractal3d_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    noise_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeTexNoise)
    noise_node.noise_type = "FRACTAL"
    noise_node.inputs[0].default_value = (0.0, 0.0, 0.0)  # Vector
    noise_node.inputs[1].default_value = 3.0  # Scale -> mapped from lacunarity
    noise_node.inputs[2].default_value = 3.0  # Detail -> mapped from octaves
    noise_node.inputs[3].default_value = 2.0  # Roughness -> mapped from lacunarity
    noise_node.inputs[4].default_value = 0.5  # Distortion -> mapped from diminish
    noise_node.update()

    amp_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMath)
    amp_node.operation = "MULTIPLY"
    amp_node.inputs[0].default_value = 0.0
    amp_node.inputs[1].default_value = 1.0
    amp_node.update()

    tree.links.new(amp_node.inputs[0], noise_node.outputs[0])

    mx_inputs = {
        "position": noise_node.inputs[0],
        "octaves": noise_node.inputs[2],
        "lacunarity": noise_node.inputs[3],
        "diminish": noise_node.inputs[4],
        "amplitude": amp_node.inputs[1],
    }
    apply_default_values(mx_node, mx_inputs)

    return (noise_node, amp_node), mx_inputs, {"out": amp_node.outputs[0]}


@register_materialx_node("ND_fractal3d_vector3")
def ND_fractal3d_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    # Use TexNoise and separate/combine to get vector3 output from scalar noise
    noise_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeTexNoise)
    noise_node.noise_type = "FRACTAL"
    noise_node.inputs[0].default_value = (0.0, 0.0, 0.0)  # Vector
    noise_node.inputs[1].default_value = 3.0  # Scale -> lacunarity
    noise_node.inputs[2].default_value = 3.0  # Detail -> octaves
    noise_node.inputs[3].default_value = 2.0  # Roughness -> lacunarity
    noise_node.inputs[4].default_value = 0.5  # Distortion -> diminish
    noise_node.update()

    combine_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeCombineXYZ)

    tree.links.new(combine_node.inputs["X"], noise_node.outputs[0])
    tree.links.new(combine_node.inputs["Y"], noise_node.outputs[0])
    tree.links.new(combine_node.inputs["Z"], noise_node.outputs[0])

    mx_inputs = {
        "position": noise_node.inputs[0],
        "octaves": noise_node.inputs[2],
        "lacunarity": noise_node.inputs[3],
        "diminish": noise_node.inputs[4],
    }
    apply_default_values(mx_node, mx_inputs)

    return (noise_node, combine_node), mx_inputs, {"out": combine_node.outputs[0]}


@register_materialx_node("ND_noise3d_float")
def ND_noise3d_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    noise_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeTexNoise)
    noise_node.noise_type = "DEFAULT"
    noise_node.inputs[0].default_value = (0.0, 0.0, 0.0)  # Vector
    noise_node.inputs[1].default_value = 5.0  # Scale
    noise_node.update()

    mx_inputs = {
        "position": noise_node.inputs[0],
        "scale": noise_node.inputs[1],
    }
    apply_default_values(mx_node, mx_inputs)

    return (noise_node,), mx_inputs, {"out": noise_node.outputs[0]}


# =============================================================================
# Channel / Conversion nodes
# =============================================================================

@register_materialx_node("ND_constant_float")
def ND_constant_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeValue)
    node.outputs[0].default_value = 0.0
    node.update()

    mx_inputs = {}
    mx_inputs["value"] = node.outputs[0]

    apply_default_values(mx_node, mx_inputs)

    return (node,), mx_inputs, {"out": node.outputs[0]}


@register_materialx_node("ND_constant_color3")
def ND_constant_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeCombineColor)
    node.inputs[0].default_value = 0.0  # R
    node.inputs[1].default_value = 0.0  # G
    node.inputs[2].default_value = 0.0  # B
    node.update()

    mx_inputs = {
        "value": node.outputs[0],
    }
    apply_default_values(mx_node, mx_inputs)

    return (node,), mx_inputs, {"out": node.outputs[0]}


@register_materialx_node("ND_constant_vector3")
def ND_constant_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeCombineXYZ)
    node.inputs[0].default_value = 0.0  # X
    node.inputs[1].default_value = 0.0  # Y
    node.inputs[2].default_value = 0.0  # Z
    node.update()

    mx_inputs = {
        "value": node.outputs[0],
    }
    apply_default_values(mx_node, mx_inputs)

    return (node,), mx_inputs, {"out": node.outputs[0]}


@register_materialx_node("ND_combine3_color3")
def ND_combine3_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeCombineColor)
    node.mode = "RGB"
    node.inputs[0].default_value = 0.0  # R
    node.inputs[1].default_value = 0.0  # G
    node.inputs[2].default_value = 0.0  # B
    node.update()

    mx_inputs = {
        "in1": node.inputs[0],
        "in2": node.inputs[1],
        "in3": node.inputs[2],
    }
    apply_default_values(mx_node, mx_inputs)

    return (node,), mx_inputs, {"out": node.outputs[0]}


@register_materialx_node("ND_separate3_color3")
def ND_separate3_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeSeparateColor)
    node.mode = "RGB"
    node.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
    node.update()

    mx_inputs = {"in": node.inputs[0]}
    apply_default_values(mx_node, mx_inputs)

    mx_outputs = {
        "outx": node.outputs[0],
        "outy": node.outputs[1],
        "outz": node.outputs[2],
    }
    return (node,), mx_inputs, mx_outputs


@register_materialx_node("ND_hsvtorgb")
def ND_hsvtorgb(tree: bpy.types.NodeTree, mx_node: mx.Node):
    """Convert HSV-encoded color3 to RGB. In MaterialX, this means taking a color3
    where the channels represent H, S, V values and outputting the equivalent RGB color.
    We use SeparateColor(HSV) -> CombineColor(RGB) which performs the conversion."""
    separate = create_blender_node(tree, mx_node, bpy.types.ShaderNodeSeparateColor)
    separate.mode = "HSV"
    separate.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
    separate.update()

    combine = create_blender_node(tree, mx_node, bpy.types.ShaderNodeCombineColor)
    combine.mode = "RGB"
    combine.inputs[0].default_value = 0.0  # R
    combine.inputs[1].default_value = 0.0  # G
    combine.inputs[2].default_value = 0.0  # B
    combine.update()

    tree.links.new(combine.inputs[0], separate.outputs[0])  # H -> R
    tree.links.new(combine.inputs[1], separate.outputs[1])  # S -> G
    tree.links.new(combine.inputs[2], separate.outputs[2])  # V -> B

    mx_inputs = {"in": separate.inputs[0]}
    apply_default_values(mx_node, mx_inputs)

    return (separate, combine), mx_inputs, {"out": combine.outputs[0]}


@register_materialx_node("ND_rgbtohsv")
def ND_rgbtohsv(tree: bpy.types.NodeTree, mx_node: mx.Node):
    """Convert RGB color3 to HSV-encoded color3. We use SeparateColor(RGB) -> CombineColor(HSV)."""
    separate = create_blender_node(tree, mx_node, bpy.types.ShaderNodeSeparateColor)
    separate.mode = "RGB"
    separate.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
    separate.update()

    combine = create_blender_node(tree, mx_node, bpy.types.ShaderNodeCombineColor)
    combine.mode = "HSV"
    combine.inputs[0].default_value = 0.0  # H
    combine.inputs[1].default_value = 0.0  # S
    combine.inputs[2].default_value = 1.0  # V
    combine.update()

    tree.links.new(combine.inputs[0], separate.outputs[0])  # R -> H
    tree.links.new(combine.inputs[1], separate.outputs[1])  # G -> S
    tree.links.new(combine.inputs[2], separate.outputs[2])  # B -> V

    mx_inputs = {"in": separate.inputs[0]}
    apply_default_values(mx_node, mx_inputs)

    return (separate, combine), mx_inputs, {"out": combine.outputs[0]}


# =============================================================================
# Texture placement
# =============================================================================

@register_materialx_node("ND_place2d_vector2")
def ND_place2d_vector2(tree: bpy.types.NodeTree, mx_node: mx.Node):
    mult_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    mult_node.operation = "MULTIPLY"
    mult_node.inputs[0].default_value = (0.0, 0.0, 0.0)
    mult_node.inputs[1].default_value = (1.0, 1.0, 1.0)
    mult_node.update()

    add_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    add_node.operation = "ADD"
    add_node.inputs[0].default_value = (0.0, 0.0, 0.0)
    add_node.inputs[1].default_value = (0.0, 0.0, 0.0)
    add_node.update()

    tree.links.new(add_node.inputs[0], mult_node.outputs[0])

    mx_inputs = {
        "texcoord": mult_node.inputs[0],
        "uvtiling": mult_node.inputs[1],
        "uvoffset": add_node.inputs[1],
    }
    apply_default_values(mx_node, mx_inputs)

    return (mult_node, add_node), mx_inputs, {"out": add_node.outputs[0]}


# =============================================================================
# Remap
# =============================================================================

@register_materialx_node("ND_remap_float")
def ND_remap_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    """Remap a value from one range to another using MapRange node."""
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMapRange)
    node.clamp = False
    node.update()

    mx_inputs = {
        "in": node.inputs["Value"],
        "frommin": node.inputs["From Min"],
        "frommax": node.inputs["From Max"],
        "tomin": node.inputs["To Min"],
        "tomax": node.inputs["To Max"],
    }
    apply_default_values(mx_node, mx_inputs)

    return (node,), mx_inputs, {"out": node.outputs["Result"]}


# =============================================================================
# Unlit surface shader
# =============================================================================

@register_materialx_node("ND_surface_unlit")
def ND_surface_unlit(tree: bpy.types.NodeTree, mx_node: mx.Node):
    """Map MaterialX surface_unlit to an Emission + Transparent shader in Blender."""
    emission = create_blender_node(tree, mx_node, bpy.types.ShaderNodeEmission)
    emission.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Color
    emission.inputs[1].default_value = 1.0  # Strength
    emission.update()

    bsdf = create_blender_node(tree, mx_node, bpy.types.ShaderNodeBsdfPrincipled)
    bsdf.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)  # Base Color
    bsdf.inputs[1].default_value = 0.0  # Metallic
    bsdf.inputs[7].default_value = (1.0, 1.0, 1.0, 1.0)  # Transmission
    bsdf.update()

    mx_inputs = {
        "emission": bsdf.inputs[16],
        "emission_color": bsdf.inputs[0],
        "transmission": bsdf.inputs[14],
        "transmission_color": bsdf.inputs[3],
        "opacity": bsdf.inputs[24],
    }
    apply_default_values(mx_node, mx_inputs)

    mx_outputs = {"out": bsdf.outputs[0]}
    return (bsdf, emission), mx_inputs, mx_outputs


# =============================================================================
# Image (non-tiled) nodes
# =============================================================================

import os


@register_materialx_node("ND_image_float")
def ND_image_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    file_input = mx_node.getInput("file")
    image_path = file_input.getValueString()
    node: bpy.types.ShaderNodeTexImage = create_blender_node(
        tree, mx_node, bpy.types.ShaderNodeTexImage
    )
    if os.path.exists(image_path):
        bl_image = bpy.data.images.load(image_path, check_existing=True)
    else:
        bl_image = bpy.data.images.new(name=image_path, width=1, height=1)
        bl_image.generated_color = (0.0, 0.0, 0.0, 1.0)
    bl_image.colorspace_settings.name = "Linear Rec.709"
    node.image = bl_image
    node.interpolation = "Linear"

    mx_inputs = {"texcoord": node.inputs["Vector"]}
    apply_default_values(mx_node, mx_inputs)

    mx_outputs = {"out": node.outputs[0]}
    return (node,), mx_inputs, mx_outputs


@register_materialx_node("ND_image_vector3")
def ND_image_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    file_input = mx_node.getInput("file")
    image_path = file_input.getValueString()
    node: bpy.types.ShaderNodeTexImage = create_blender_node(
        tree, mx_node, bpy.types.ShaderNodeTexImage
    )
    if os.path.exists(image_path):
        bl_image = bpy.data.images.load(image_path, check_existing=True)
    else:
        bl_image = bpy.data.images.new(name=image_path, width=1, height=1)
        bl_image.generated_color = (0.0, 0.0, 0.0, 1.0)
    bl_image.colorspace_settings.name = "Linear Rec.709"
    node.image = bl_image
    node.interpolation = "Linear"

    mx_inputs = {"texcoord": node.inputs["Vector"]}
    apply_default_values(mx_node, mx_inputs)

    mx_outputs = {"out": node.outputs[0]}
    return (node,), mx_inputs, mx_outputs
