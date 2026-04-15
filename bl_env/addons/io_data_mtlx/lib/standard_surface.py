# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import bpy
import MaterialX as mx

from .graph_utils import apply_default_values, create_blender_node
from .node_registry import register_materialx_node


@register_materialx_node("ND_standard_surface_surfaceshader")
def ND_standard_surface_surfaceshader(
    tree: bpy.types.NodeTree, mx_node: mx.Node
):
    ShaderNodeBsdfPrincipled_2 = create_blender_node(
        tree, mx_node, "ShaderNodeBsdfPrincipled"
    )
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[0].default_value = (
        0.800000011920929,
        0.800000011920929,
        0.800000011920929,
        1.0,
    )
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[1].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[2].default_value = 0.5
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[3].default_value = 1.4500000476837158
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[4].default_value = 1.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[5].default_value = (0.0, 0.0, 0.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[7].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[8].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[9].default_value = (
        1.0,
        0.20000000298023224,
        0.10000000149011612,
    )
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[10].default_value = 0.05000000074505806
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[12].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[13].default_value = 0.5
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[15].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[16].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[17].default_value = (0.0, 0.0, 0.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[18].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[19].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[20].default_value = 0.029999999329447746
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[21].default_value = 1.5
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[23].default_value = (0.0, 0.0, 0.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[24].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[25].default_value = 0.5
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[28].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[29].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs[30].default_value = 1.3300000429153442
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeMix_3 = create_blender_node(tree, mx_node, "ShaderNodeMix")
    ShaderNodeMix_3.update()
    ShaderNodeMix_3.data_type = "RGBA"
    ShaderNodeMix_3.update()
    ShaderNodeMix_3.blend_type = "MULTIPLY"
    ShaderNodeMix_3.update()
    ShaderNodeMix_3.inputs[0].default_value = 1.0
    ShaderNodeMix_3.update()
    ShaderNodeMix_3.inputs[6].default_value = (
        0.6038432121276855,
        0.603837251663208,
        0.6038312911987305,
        1.0,
    )
    ShaderNodeMix_3.update()
    ShaderNodeMix_3.inputs[7].default_value = (0.5, 0.5, 0.5, 1.0)
    ShaderNodeMix_3.update()
    ShaderNodeHueSaturation_4 = create_blender_node(
        tree, mx_node, "ShaderNodeHueSaturation"
    )
    ShaderNodeHueSaturation_4.update()
    ShaderNodeHueSaturation_4.inputs[0].default_value = 0.0
    ShaderNodeHueSaturation_4.update()
    ShaderNodeHueSaturation_4.inputs[1].default_value = 1.0
    ShaderNodeHueSaturation_4.update()
    ShaderNodeHueSaturation_4.inputs[2].default_value = 1.0
    ShaderNodeHueSaturation_4.update()
    ShaderNodeHueSaturation_4.inputs[3].default_value = 1.0
    ShaderNodeHueSaturation_4.update()
    ShaderNodeHueSaturation_4.inputs[4].default_value = (
        0.9971059560775757,
        1.0,
        1.0,
        1.0,
    )
    ShaderNodeHueSaturation_4.update()
    ShaderNodeMix_5 = create_blender_node(tree, mx_node, "ShaderNodeMix")
    ShaderNodeMix_5.update()
    ShaderNodeMix_5.data_type = "RGBA"
    ShaderNodeMix_5.update()
    ShaderNodeMix_5.blend_type = "MULTIPLY"
    ShaderNodeMix_5.update()
    ShaderNodeMix_5.inputs[0].default_value = 1.0
    ShaderNodeMix_5.update()
    ShaderNodeMix_5.inputs[6].default_value = (
        0.6038432121276855,
        0.603837251663208,
        0.6038312911987305,
        1.0,
    )
    ShaderNodeMix_5.update()
    ShaderNodeMix_5.inputs[7].default_value = (0.5, 0.5, 0.5, 1.0)
    ShaderNodeMix_5.update()
    ShaderNodeHueSaturation_6 = create_blender_node(
        tree, mx_node, "ShaderNodeHueSaturation"
    )
    ShaderNodeHueSaturation_6.update()
    ShaderNodeHueSaturation_6.inputs[0].default_value = 0.0
    ShaderNodeHueSaturation_6.update()
    ShaderNodeHueSaturation_6.inputs[1].default_value = 1.0
    ShaderNodeHueSaturation_6.update()
    ShaderNodeHueSaturation_6.inputs[2].default_value = 1.0
    ShaderNodeHueSaturation_6.update()
    ShaderNodeHueSaturation_6.inputs[3].default_value = 1.0
    ShaderNodeHueSaturation_6.update()
    ShaderNodeHueSaturation_6.inputs[4].default_value = (
        0.9971059560775757,
        1.0,
        1.0,
        1.0,
    )
    ShaderNodeHueSaturation_6.update()
    mx_node_inputs = {}
    mx_node_outputs = {}
    mx_node_outputs["out"] = ShaderNodeBsdfPrincipled_2.outputs[0]
    tree.links.new(
        ShaderNodeMix_3.outputs[2], ShaderNodeBsdfPrincipled_2.inputs[0]
    )
    mx_node_inputs["base"] = ShaderNodeHueSaturation_4.inputs[2]
    tree.links.new(
        ShaderNodeHueSaturation_4.outputs[0], ShaderNodeMix_3.inputs[6]
    )
    mx_node_inputs["base_color"] = ShaderNodeMix_3.inputs[7]
    mx_node_inputs["metalness"] = ShaderNodeBsdfPrincipled_2.inputs[1]
    mx_node_inputs["diffuse_roughness"] = ShaderNodeBsdfPrincipled_2.inputs[7]
    tree.links.new(
        ShaderNodeHueSaturation_6.outputs[0], ShaderNodeMix_5.inputs[6]
    )
    mx_node_inputs["specular"] = ShaderNodeHueSaturation_6.inputs[2]
    mx_node_inputs["specular_color"] = ShaderNodeMix_5.inputs[7]
    tree.links.new(
        ShaderNodeMix_5.outputs[2], ShaderNodeBsdfPrincipled_2.inputs[14]
    )
    mx_node_inputs["specular_IOR"] = ShaderNodeBsdfPrincipled_2.inputs[13]
    mx_node_inputs["specular_anisotropy"] = ShaderNodeBsdfPrincipled_2.inputs[
        15
    ]
    mx_node_inputs["specular_rotation"] = ShaderNodeBsdfPrincipled_2.inputs[16]
    mx_node_inputs["specular_roughness"] = ShaderNodeBsdfPrincipled_2.inputs[2]
    mx_node_inputs["transmission"] = ShaderNodeBsdfPrincipled_2.inputs[18]
    mx_node_inputs["subsurface"] = ShaderNodeBsdfPrincipled_2.inputs[8]
    mx_node_inputs["subsurface_radius"] = ShaderNodeBsdfPrincipled_2.inputs[9]
    mx_node_inputs["subsurface_scale"] = ShaderNodeBsdfPrincipled_2.inputs[10]
    mx_node_inputs["subsurface_anisotropy"] = (
        ShaderNodeBsdfPrincipled_2.inputs[12]
    )
    mx_node_inputs["sheen"] = ShaderNodeBsdfPrincipled_2.inputs[24]
    mx_node_inputs["sheen_color"] = ShaderNodeBsdfPrincipled_2.inputs[26]
    mx_node_inputs["sheen_roughness"] = ShaderNodeBsdfPrincipled_2.inputs[25]
    mx_node_inputs["coat"] = ShaderNodeBsdfPrincipled_2.inputs[19]
    mx_node_inputs["coat_color"] = ShaderNodeBsdfPrincipled_2.inputs[22]
    mx_node_inputs["coat_roughness"] = ShaderNodeBsdfPrincipled_2.inputs[20]
    mx_node_inputs["coat_ior"] = ShaderNodeBsdfPrincipled_2.inputs[21]
    mx_node_inputs["coat_normal"] = ShaderNodeBsdfPrincipled_2.inputs[23]
    mx_node_inputs["thin_film_thickness"] = ShaderNodeBsdfPrincipled_2.inputs[
        29
    ]
    mx_node_inputs["thin_film_IOR"] = ShaderNodeBsdfPrincipled_2.inputs[30]
    mx_node_inputs["emission"] = ShaderNodeBsdfPrincipled_2.inputs[28]
    mx_node_inputs["emission_color"] = ShaderNodeBsdfPrincipled_2.inputs[27]
    mx_node_inputs["normal"] = ShaderNodeBsdfPrincipled_2.inputs[5]
    mx_node_inputs["tangent"] = ShaderNodeBsdfPrincipled_2.inputs[17]
    apply_default_values(mx_node, mx_node_inputs)
    return (
        (
            ShaderNodeBsdfPrincipled_2,
            ShaderNodeMix_3,
            ShaderNodeHueSaturation_4,
            ShaderNodeMix_5,
            ShaderNodeHueSaturation_6,
        ),
        mx_node_inputs,
        mx_node_outputs,
    )
