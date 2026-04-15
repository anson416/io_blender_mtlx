# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import bpy
from bpy.props import CollectionProperty, StringProperty
from bpy.types import Material, PropertyGroup

from . import materialx_handle as mxhandle

if TYPE_CHECKING:

    class Material(bpy.types.Material):
        mtlx_inputs: CollectionProperty[PG_MTLXInput]
        mtlx_document: StringProperty


logger = logging.getLogger(__name__)


class PG_ValueType(PropertyGroup):
    BOOLEAN: bpy.props.BoolProperty(
        name="Boolean", default=False, update=on_update_mtlx_inputs
    )
    FLOAT: bpy.props.FloatProperty(
        name="Float", default=0.0, update=on_update_mtlx_inputs
    )
    INTEGER: bpy.props.IntProperty(
        name="Integer", default=0, update=on_update_mtlx_inputs
    )
    STRING: bpy.props.StringProperty(
        name="String", default="", update=on_update_mtlx_inputs
    )
    FILENAME: bpy.props.StringProperty(
        name="Filename",
        default="",
        subtype="FILE_PATH",
        update=on_update_mtlx_inputs,
    )
    COLOR4: bpy.props.FloatVectorProperty(
        name="Color4",
        default=(0.0, 0.0, 0.0, 0.0),
        size=4,
        subtype="COLOR",
        update=on_update_mtlx_inputs,
    )
    COLOR3: bpy.props.FloatVectorProperty(
        name="Color3",
        default=(0.0, 0.0, 0.0),
        size=3,
        subtype="COLOR",
        update=on_update_mtlx_inputs,
    )
    VECTOR4: bpy.props.FloatVectorProperty(
        name="Vector4",
        default=(0.0, 0.0, 0.0, 0.0),
        size=4,
        update=on_update_mtlx_inputs,
    )
    VECTOR3: bpy.props.FloatVectorProperty(
        name="Vector3",
        default=(0.0, 0.0, 0.0),
        size=3,
        update=on_update_mtlx_inputs,
    )
    VECTOR2: bpy.props.FloatVectorProperty(
        name="Vector2",
        default=(0.0, 0.0),
        size=2,
        update=on_update_mtlx_inputs,
    )
    MATRIX33: bpy.props.FloatVectorProperty(
        name="Matrix33",
        default=(0.0,) * 9,
        size=9,
        update=on_update_mtlx_inputs,
    )
    MATRIX44: bpy.props.FloatVectorProperty(
        name="Matrix",
        default=(0.0,) * 16,
        size=16,
        update=on_update_mtlx_inputs,
    )
    customized: bpy.props.BoolProperty(name="Customized", default=False)


class PG_MTLXInput(PropertyGroup):
    name: bpy.props.StringProperty(name="Name")
    node_name: bpy.props.StringProperty(name="Node")
    value_string: bpy.props.StringProperty(name="Value")
    prop_type: bpy.props.StringProperty(name="Type", options={"HIDDEN"})
    value: bpy.props.PointerProperty(type=PG_ValueType, name="Value Type")


def on_update_mtlx_document(self, context):
    # Placeholder for any logic needed when the MTLX document is updated
    logger.info("MTLX Document updated: %s", self.mtlx_document)
    handle = mxhandle.get_material_handler(self)
    handle.load_document()


def on_update_mtlx_inputs(self, context):
    # Placeholder for any logic needed when MTLX inputs are updated
    handle = mxhandle.get_material_handler(self.id_data)
    self.customized = True
    if handle.document:
        handle.on_blender_inputs_update()


mtlx_document = StringProperty(
    name="MTLX Document",
    description="Path to the MTLX document",
    default="",
    maxlen=1024,
    subtype="FILE_PATH",
    update=on_update_mtlx_document,
)


def register():
    bpy.utils.register_class(PG_ValueType)
    bpy.utils.register_class(PG_MTLXInput)
    Material.mtlx_inputs = CollectionProperty(type=PG_MTLXInput)
    Material.mtlx_document = mtlx_document


def unregister():
    del Material.mtlx_inputs
    del Material.mtlx_document
    bpy.utils.unregister_class(PG_MTLXInput)
    bpy.utils.unregister_class(PG_ValueType)
