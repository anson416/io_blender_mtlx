# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import bpy

from . import material_properties as mp
from . import materialx_handle as mh


class MTLXDocumentPicker(bpy.types.Operator):
    bl_idname = "material.mtlx_pick_document"
    bl_label = "Pick MTLX Document"
    bl_description = "Pick a MaterialX document file"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(
        default="*.mtlx;*.MTLX",
        options={"HIDDEN"},
    )

    def execute(self, context):
        material: mp.Material = context.material
        if not material:
            self.report({"WARNING"}, "No material found")
            return {"CANCELLED"}

        material.mtlx_document = self.filepath
        mh.get_material_handler(material)
        self.report({"INFO"}, f"Set MTLX document to {self.filepath}")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class RevertValue(bpy.types.Operator):
    bl_idname = "material.mtlx_revert_value"
    bl_label = "Revert MTLX Input Value"
    bl_description = (
        "Revert the MTLX input value to the original value from the document"
    )
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    input_name: bpy.props.StringProperty(name="Input Name")
    node_name: bpy.props.StringProperty(name="Node Name")

    def execute(self, context):
        material: mp.Material = context.material
        if not material:
            self.report({"WARNING"}, "No material found")
            return {"CANCELLED"}

        handle = mh.get_material_handler(material)
        if not handle or not handle.document:
            self.report({"WARNING"}, "No MTLX document loaded")
            return {"CANCELLED"}

        for _input in handle.inputs:
            if (
                _input.name != self.input_name
                or _input.node_name != self.node_name
            ):
                continue
            bl_value = material.mtlx_inputs.get(_input.name)
            if not bl_value:
                continue
            bl_value.value[bl_value.prop_type] = mh.CONVERT_TYPE_MAP[
                bl_value.prop_type.upper()
            ](_input.value.getData())
            bl_value.value.customized = False
            handle.on_blender_inputs_update()
            self.report({"INFO"}, f"Reverted value of input '{_input.name}'")
            return {"FINISHED"}

        self.report({"WARNING"}, f"Input '{self.input_name}' not found")
        return {"CANCELLED"}


class MTLXMaterialPanel(bpy.types.Panel):
    bl_label = "MTLX Material Properties"
    bl_idname = "MATERIAL_PT_mtlx_properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_order = 1
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
        material: mp.Material = context.material

        if not material:
            return

        row = layout.row()
        row.operator(
            MTLXDocumentPicker.bl_idname,
            text=material.mtlx_document
            if material.mtlx_document
            else "Pick a Document to get started",
            icon="FILE_FOLDER"
            if not material.mtlx_document
            else "MATSHADERBALL",
        )

        if not hasattr(material, "mtlx_inputs"):
            return
        inputs = material.mtlx_inputs
        if not inputs:
            return

        row = layout.row()
        row.label(text="Inputs:")

        layout.use_property_split = True
        layout.use_property_decorate = False

        node_names = list(set([input.node_name for input in inputs]))
        node_names.sort()
        for node_name in node_names:
            column = layout.column()
            column.label(text=f"Node: {node_name}", icon="NODE_MATERIAL")
            self.draw_inputs(column, inputs, node_name)

    def draw_inputs(self, layout, inputs, node_name):
        for input in inputs:
            if input.node_name != node_name:
                continue
            row = layout.row()
            row.prop(input.value, input.prop_type, text=input.name)
            sub_column = row.column()
            sub_column.enabled = input.value.customized
            operator = sub_column.operator(
                "material.mtlx_revert_value", text="", icon="LOOP_BACK"
            )
            operator.input_name = input.name
            operator.node_name = input.node_name


def register():
    bpy.utils.register_class(MTLXDocumentPicker)
    bpy.utils.register_class(RevertValue)
    bpy.utils.register_class(MTLXMaterialPanel)


def unregister():
    bpy.utils.unregister_class(MTLXMaterialPanel)
    bpy.utils.unregister_class(RevertValue)
    bpy.utils.unregister_class(MTLXDocumentPicker)
