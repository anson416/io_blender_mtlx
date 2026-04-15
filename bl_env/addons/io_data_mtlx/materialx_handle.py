# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import logging
import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import bpy
import MaterialX as mx

logger = logging.getLogger(__name__)

if TYPE_CHECKING:

    class TypedValue(mx.Value):
        def getData(self) -> Any: ...


from . import material_generate
from . import material_properties as mp


@dataclass
class MTLXInput:
    name: str
    node_name: str
    value_string: str
    prop_type: str
    value: "TypedValue"
    node_graph: bool = False


CONVERT_TYPE_MAP = {
    "BOOLEAN": bool,
    "FLOAT": float,
    "INTEGER": int,
    "STRING": str,
    "FILENAME": str,
    "COLOR4": list,
    "COLOR3": list,
    "VECTOR4": list,
    "VECTOR3": list,
    "VECTOR2": list,
    "MATRIX33": list,
    "MATRIX44": list,
}


CAST_BL_TO_MTLX_TYPE_MAP = {
    "BOOLEAN": bool,
    "FLOAT": float,
    "INTEGER": int,
    "STRING": str,
    "FILENAME": str,
    "COLOR4": lambda x: mx.Color4(list(x)),
    "COLOR3": lambda x: mx.Color3(list(x)),
    "VECTOR4": lambda x: mx.Vector4(list(x)),
    "VECTOR3": lambda x: mx.Vector3(list(x)),
    "VECTOR2": lambda x: mx.Vector2(list(x)),
    "MATRIX33": lambda x: mx.Matrix33(list(x)),
    "MATRIX44": lambda x: mx.Matrix44(list(x)),
}


class MaterialXHandle:
    def __init__(self, material: mp.Material):
        self._material: mp.Material = material
        self.inputs: list[MTLXInput] = (
            None  # will be populated by load_document
        )
        self.document: mx.Document = None

    @property
    def material(self) -> mp.Material:
        material = None
        try:
            self._material.mtlx_document
            material = self._material
        except ReferenceError:
            pass
        if material:
            return material
        session = None
        for session, material_handle in MATERIAL_HANDLERS.items():
            if self is material_handle:
                break
        for mat in bpy.data.materials:
            if mat.session_uid == session:
                material = mat
                break
        self._material = material
        return material

    def load_document(self):
        """Load a MaterialX document from the given file path."""
        material = self.material
        filepath = material.mtlx_document
        if not filepath or not os.path.isfile(filepath):
            self.document = None
            self.inputs = []
            self.update_material_inputs()
            return
        try:
            self.document = mx.createDocument()
            # mx.loadLibraries(mx.getDefaultDataLibraryFolders(), mx.getDefaultDataSearchPath(), self.document)
            mx.readFromXmlFileBase(self.document, filepath)
            logger.info("Loaded MaterialX document from %s", filepath)
        except Exception as e:
            logger.error("Failed to load MaterialX document: %s", e)
        self.get_inputs()
        self.update_material_inputs()
        self.on_blender_inputs_update()

    def get_inputs(self) -> list[MTLXInput]:
        """Get the inputs defined in the MaterialX document."""
        self.inputs = []
        if not self.document:
            return
        for node in self.document.getNodes():
            self.inputs.extend(self.get_inputs_from_node(node))
        for node in self.document.getNodeGraphs():
            self.inputs.extend(self.get_inputs_from_node(node))

    def get_inputs_from_node(
        self, node: mx.Node | mx.NodeGraph
    ) -> list[MTLXInput]:
        """Get the inputs defined in a specific node or node graph."""
        inputs = []
        for _input in node.getInputs():
            if _input.getConnectedNode() or _input.getConnectedOutput():
                continue
            inputs.append(
                MTLXInput(
                    name=_input.getName(),
                    node_name=node.getName(),
                    value_string=_input.getValueString(),
                    prop_type=_input.getType(),
                    node_graph=isinstance(node, mx.NodeGraph),
                    value=_input._getValue(),
                )
            )
        return inputs

    def update_material_inputs(self):
        self._remove_material_inputs()
        self._add_material_inputs()

    def _remove_material_inputs(self):
        """remove any inputs from blender's interface that are no longer in the document"""
        document_inputs = {
            (inp.name, inp.node_name, inp.prop_type.upper())
            for inp in self.inputs
        }
        mark_for_removal = []
        for i, _input in enumerate(self.material.mtlx_inputs):
            _input: mp.PG_MTLXInput
            if (
                _input.name,
                _input.node_name,
                _input.prop_type.upper(),
            ) not in document_inputs:
                mark_for_removal.append(i)
                continue
            if not _input.value.customized:
                mark_for_removal.append(i)
        for i in reversed(mark_for_removal):
            self.material.mtlx_inputs.remove(i)

    def _add_material_inputs(self):
        """add any new inputs from the document to blender's interface"""
        blender_inputs = {
            (inp.name, inp.node_name) for inp in self.material.mtlx_inputs
        }
        for i, _input in enumerate(self.inputs):
            if (_input.name, _input.node_name) in blender_inputs:
                continue
            mtlx_input: mp.PG_MTLXInput = self.material.mtlx_inputs.add()
            mtlx_input.name = _input.name
            mtlx_input.node_name = _input.node_name
            mtlx_input.value_string = _input.value_string
            mtlx_input.prop_type = _input.prop_type.upper()
            mtlx_input.value[_input.prop_type.upper()] = CONVERT_TYPE_MAP[
                _input.prop_type.upper()
            ](_input.value.getData())
            self.material.mtlx_inputs.move(
                len(self.material.mtlx_inputs) - 1, i
            )

    def on_blender_inputs_update(self):
        """If any of the blender inputs have changed, update the MaterialX document accordingly.
        Then trigger a re-generation of the material in Blender."""
        for _input in self.inputs:
            if _input.node_graph:
                node = self.document.getNodeGraph(_input.node_name)
            else:
                node = self.document.getNode(_input.node_name)

            blnd_input_value = self._get_value_from_blender_input(
                _input.name, _input.node_name
            )
            if blnd_input_value is None:
                continue
            value = CAST_BL_TO_MTLX_TYPE_MAP[_input.prop_type.upper()](
                blnd_input_value
            )

            mx_input = node.getInput(_input.name)
            self._set_value_to_mx_input(mx_input, value)
        material_generate.generate_material(self.material)

    def _get_value_from_blender_input(self, name: str, node_name: str) -> Any:
        """Get the value of a specific input from Blender's material properties."""
        for bl_input in self.material.mtlx_inputs:
            bl_input: mp.PG_MTLXInput
            if bl_input.name == name and bl_input.node_name == node_name:
                return bl_input.value[bl_input.prop_type.upper()]
        return None

    def _set_value_to_mx_input(self, mx_input: mx.Input, value: Any):
        """Set the value of a MaterialX input based on the type."""
        prop_type = mx_input.getType()
        if prop_type == "filename":
            prop_type = "string"
        method_name = f"_setValue{prop_type}"
        set_mx_input_value = getattr(mx_input, method_name)
        set_mx_input_value(value)


MATERIAL_HANDLERS: dict[int, MaterialXHandle] = {}
# key is bpy.data.materials[0].session_uid


def get_material_handler(material: mp.Material) -> MaterialXHandle:
    if material.session_uid not in MATERIAL_HANDLERS:
        _add_material_handler(material)
    return MATERIAL_HANDLERS[material.session_uid]


def _add_material_handler(material: mp.Material):
    MATERIAL_HANDLERS[material.session_uid] = MaterialXHandle(material)
    MATERIAL_HANDLERS[material.session_uid].load_document()


@bpy.app.handlers.persistent
def startup(_):
    for material in bpy.data.materials:
        _add_material_handler(material)


def register():
    bpy.app.handlers.load_post.append(startup)


def unregister():
    bpy.app.handlers.load_post.remove(startup)
