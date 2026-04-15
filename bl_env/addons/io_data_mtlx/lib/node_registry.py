# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import bpy
    import MaterialX as mx

    return_value = tuple[
        tuple[bpy.types.Node, ...],
        dict[str, bpy.types.NodeSocket],
        dict[str, bpy.types.NodeSocket],
    ]


materialx_nodes = {}


def register_materialx_node(node_definition: str):
    """
    Decorator to register a MaterialX node definition.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(
            tree: bpy.types.NodeTree, mx_node: mx.Node, *args, **kwargs
        ) -> return_value:
            return func(tree, mx_node, *args, **kwargs)

        materialx_nodes[node_definition] = wrapper
        return wrapper

    return decorator
