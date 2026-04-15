# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import bpy
import bpy.types

# Make 'pxr' module available, for running as 'bpy' PIP package.
bpy.utils.expose_bundled_modules()

import MaterialX as mx
import pxr.Gf as Gf
import pxr.Sdf as Sdf
import pxr.Usd as Usd
import pxr.UsdShade as UsdShade

from . import materialx_handle as mh

"""
//     def Scope "MaterialX"
//     {
//         def Material "surfacematerial" (
//             prepend references = @./basic_material.mtlx@</MaterialX/Materials/surfacematerial>
//         )
//         {
//             color3f inputs:diffuseColor = (0, 0, 1)
//         }
//     }
"""


def convert_mtlx_token_to_usd_type(mtlx_type: str) -> Sdf.ValueTypeName:
    """https://github.com/PixarAnimationStudios/OpenUSD/blob/dev/pxr/usd/usdMtlx/utils.cpp#L529C1-L551C71"""
    mapping = {
        "boolean": (Sdf.ValueTypeNames.Bool, False, bool),
        "color3array": (Sdf.ValueTypeNames.Color3fArray, True, Gf.Vec3f),
        "color3": (Sdf.ValueTypeNames.Color3f, True, Gf.Vec3f),
        "color4array": (Sdf.ValueTypeNames.Color4fArray, True, Gf.Vec4f),
        "color4": (Sdf.ValueTypeNames.Color4f, True, Gf.Vec4f),
        "filename": (Sdf.ValueTypeNames.Asset, False, str),
        "floatarray": (Sdf.ValueTypeNames.FloatArray, True, float),
        "float": (Sdf.ValueTypeNames.Float, False, float),
        "geomnamearray": (Sdf.ValueTypeNames.StringArray, True, str),
        "geomname": (Sdf.ValueTypeNames.String, False, str),
        "integerarray": (Sdf.ValueTypeNames.IntArray, True, int),
        "integer": (Sdf.ValueTypeNames.Int, False, int),
        "matrix33": (Sdf.ValueTypeNames.Matrix3d, True, Gf.Matrix3f),
        "matrix44": (Sdf.ValueTypeNames.Matrix4d, True, Gf.Matrix4f),
        "stringarray": (Sdf.ValueTypeNames.StringArray, True, str),
        "string": (Sdf.ValueTypeNames.String, False, str),
        "surfaceshader": (Sdf.ValueTypeNames.Token, False, str),
        "vector2array": (Sdf.ValueTypeNames.Float2Array, True, Gf.Vec2f),
        "vector2": (Sdf.ValueTypeNames.Float2, True, Gf.Vec2f),
        "vector3array": (Sdf.ValueTypeNames.Float3Array, True, Gf.Vec3f),
        "vector3": (Sdf.ValueTypeNames.Float3, True, Gf.Vec3f),
        "vector4array": (Sdf.ValueTypeNames.Float4Array, True, Gf.Vec4f),
        "vector4": (Sdf.ValueTypeNames.Float4, True, Gf.Vec4f),
    }
    return mapping.get(mtlx_type)


class USDMTLXRefHook(bpy.types.USDHook):
    """Example implementation of USD IO hooks"""

    bl_idname = "usd_mtlx_ref_hook"
    bl_label = "MTLX Reference Hook"

    @staticmethod
    def on_export(export_context):
        """Include the Blender filepath in the root layer custom data."""

        stage: Usd.Stage = export_context.get_stage()

        if stage is None:
            return False
        data = bpy.data
        if data is None:
            return False

        for prim in stage.TraverseAll():
            if not prim.IsA(UsdShade.Material):
                continue
            for attr in prim.GetAttributes():
                if not "blender:data_name" in attr.GetName():
                    continue
                data_name = attr.Get(Usd.TimeCode.Default())
                if not data_name in data.materials:
                    continue
                material = data.materials[data_name]
                if not hasattr(material, "mtlx_document"):
                    continue
                doc: mx.Document = mx.createDocument()
                mx.readFromXmlFileBase(doc, material.mtlx_document)
                material_name = "surfacematerial"
                if doc.getNodes("surfacematerial"):
                    material_name = doc.getNodes("surfacematerial")[
                        0
                    ].getName()
                prim.GetReferences().AddReference(
                    material.mtlx_document,
                    f"/MaterialX/Materials/{material_name}",
                )

                handle = mh.get_material_handler(material)
                handle.get_inputs()
                for _input in handle.inputs:
                    # doesn't handle skipping default values yet

                    usd_type, is_array, gf_class = (
                        convert_mtlx_token_to_usd_type(_input.prop_type)
                    )

                    value = _input.value.getData()
                    if value is None:
                        continue
                    if isinstance(value, str):
                        # cutting empty filepaths out
                        if not value:
                            continue
                    if is_array:
                        value = list(_input.value.getData().asTuple())
                    attribute = prim.CreateAttribute(
                        f"inputs:{_input.name}", usd_type
                    )
                    attribute.Set(gf_class(value), Usd.TimeCode.Default())

        return True

    @staticmethod
    def on_import(import_context):
        """Create a text object to display the stage's custom data."""
        stage = import_context.get_stage()


def register():
    bpy.utils.register_class(USDMTLXRefHook)


def unregister():
    bpy.utils.unregister_class(USDMTLXRefHook)
