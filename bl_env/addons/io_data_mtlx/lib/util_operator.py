# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import bpy


def create_node_def_code(context: bpy.types.Context) -> str:
    mapping = {}

    active_node_group = None
    for area in context.screen.areas:
        for space in area.spaces:
            if space.type == "NODE_EDITOR":
                active_node_group = space.edit_tree
                break
    if not active_node_group:
        raise ValueError("No active node group found in the current context.")
    group_name = active_node_group.name

    output = [f'@register_materialx_node("{group_name}")']
    output.append(
        f"def {group_name}(tree: bpy.types.NodeTree, mx_node: mx.Node):"
    )

    for i, node in enumerate(active_node_group.nodes):
        _type: str = type(node).__name__
        node_name = f"{_type}_{i}"
        if _type in ("NodeGroupInput", "NodeGroupOutput"):
            continue
        output.append(
            f"    {node_name} = create_blender_node(tree, mx_node, '{_type}')"
        )
        output.append(f"    {node_name}.update()")
        if hasattr(node, "data_type"):
            output.append(f"    {node_name}.data_type = '{node.data_type}'")
            output.append(f"    {node_name}.update()")
        if hasattr(node, "blend_type"):
            output.append(f"    {node_name}.blend_type = '{node.blend_type}'")
            output.append(f"    {node_name}.update()")
        if hasattr(node, "mode"):
            output.append(f"    {node_name}.mode = '{node.mode}'")
            output.append(f"    {node_name}.update()")
        for _input in node.inputs:
            _input: bpy.types.NodeSocket

            if _input.is_unavailable:
                continue
            if hasattr(_input, "default_value"):
                index = _input.path_from_id().rsplit("[")[-1][:-1]
                if isinstance(_input.default_value, int) or isinstance(
                    _input.default_value, float
                ):
                    output.append(
                        f"    {node_name}.inputs[{index}].default_value = {_input.default_value}"
                    )
                elif isinstance(_input.default_value, str):
                    output.append(
                        f"    {node_name}.inputs[{index}].default_value = '{_input.default_value}'"
                    )
                else:
                    output.append(
                        f"    {node_name}.inputs[{index}].default_value = {tuple(_input.default_value)}"
                    )
                output.append(f"    {node_name}.update()")
        mapping[node.name] = f"{node_name}"

    output.append("    mx_node_inputs = {}")
    output.append("    mx_node_outputs = {}")

    for link in active_node_group.links:
        from_node_name = link.from_node.name
        from_node_type = link.from_node.type

        from_socket_id = link.from_socket.path_from_id().rsplit("[")[-1][
            :-1
        ]  # hacky way to get the socket index
        from_socket_name = link.from_socket.name

        to_node_name = link.to_node.name
        to_node_type = link.to_node.type

        to_socket_id = link.to_socket.path_from_id().rsplit("[")[-1][:-1]
        to_socket_name = link.to_socket.name

        if from_node_type == "GROUP_INPUT":
            output.append(
                f"    mx_node_inputs['{from_socket_name}'] = {mapping[to_node_name]}.inputs[{to_socket_id}]"
            )
            continue
        if to_node_type == "GROUP_OUTPUT":
            output.append(
                f"    mx_node_outputs['{to_socket_name}'] = {mapping[from_node_name]}.outputs[{from_socket_id}]"
            )
            continue
        output.append(
            f"    tree.links.new({mapping[from_node_name]}.outputs[{from_socket_id}], {mapping[to_node_name]}.inputs[{to_socket_id}])"
        )

    output.append("    apply_default_values(mx_node, mx_node_inputs)")

    output.append(
        f"    return ({','.join(mapping.values())}), mx_node_inputs, mx_node_outputs"
    )

    return "\n".join(output)


class PrintClass(bpy.types.Operator):
    """Print the class name of the operator"""

    bl_idname = "node_tree.print_class"
    bl_label = "Print Python Code for Node Tree"

    def execute(self, context):
        self.report(
            {"INFO"},
            "Generated Python code for the active node tree. Check the console.",
        )
        print(create_node_def_code(context))
        return {"FINISHED"}


def register():
    bpy.utils.register_class(PrintClass)


def unregister():
    bpy.utils.unregister_class(PrintClass)
