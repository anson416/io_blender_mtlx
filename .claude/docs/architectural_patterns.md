# Architectural Patterns

Patterns that recur across multiple files in `bl_env/addons/io_data_mtlx/`.

## Decorator-Based Node Registry

**File**: `lib/node_registry.py`

A global dictionary `materialx_nodes` maps MaterialX node definition strings (e.g., `"ND_image_color3"`) to Python functions via the `@register_materialx_node()` decorator:

- Each registered function receives `(tree: bpy.types.NodeTree, mx_node: mx.Node)` and returns a 3-tuple: `(tuple_of_created_blender_nodes, mx_node_inputs_dict, mx_node_outputs_dict)`
- The 3-tuple return convention enables the two-pass graph generation in `material_generate.py`: Pass 1 collects nodes, Pass 2 resolves connections using the input/output dicts
- Keys are looked up dynamically during generation — unmapped definitions are skipped with a `logger.warning`

## PropertyGroup Data Model with Update Callbacks

**File**: `material_properties.py`

Two PropertyGroups are attached to `bpy.types.Material`:

- **`PG_ValueType`**: One property per MaterialX type (BOOLEAN, FLOAT, COLOR3, VECTOR3, etc.) + a `customized` flag. Each property has `update=on_update_mtlx_inputs` callback.
- **`PG_MTLXInput`**: Metadata (name, node_name, value_string, prop_type) + PointerProperty to a `PG_ValueType` instance.

The `Material.mtlx_inputs` CollectionProperty and `Material.mtlx_document` StringProperty drive the entire data flow — changing any property triggers the sync pipeline via its `update=` callback.

## Lazy-Initialized Handle with Session-UID Cache

**File**: `materialx_handle.py`

`get_material_handler()` looks up a `MaterialXHandle` by `material.session_uid` in the global `MATERIAL_HANDLERS` dict. If absent, creates one on demand. A persistent `@bpy.app.handlers.persistent startup()` handler rebuilds all handlers after file load, since `session_uid` changes when Blender reloads a `.blend`.

## Bidirectional Type Maps

**Files**: `materialx_handle.py` (CONVERT_TYPE_MAP, CAST_BL_TO_MTLX_TYPE_MAP), `usd_io.py` (convert_mtlx_token_to_usd_type), `lib/graph_utils.py` (cast_value_to_socket_type)

Three parallel type mapping systems exist:
- MaterialX native types → Python types (for reading values from the document)
- Blender socket values → MaterialX types (for writing values back)
- MaterialX type tokens → USD Sdf.ValueTypeNames (for USD export)

`cast_value_to_socket_type()` in `lib/graph_utils.py` handles the runtime conversion: padding Vector2 to 3-tuple, expanding Color3 to RGBA, converting bools to 1.0/0.0, etc.

## Two-Pass Node Graph Generation

**File**: `material_generate.py`

The `generate_material()` function separates node creation from connection:
- **Pass 1**: Iterate `doc.getNodes()`, look up each in the registry, instantiate Blender nodes. Store results in `node_mapping`.
- **Pass 2**: Iterate nodes again, resolve `mx.Input.getConnectedNode()` / `getConnectedOutput()`, create `tree.links.new()`.

This decouples node identity from wiring order, allowing circular or forward references.

## Recursive Default Value Resolution

**File**: `lib/graph_utils.py`

`node_declaration_get_default_values()` walks a node definition's `getInheritsFrom()` chain recursively to accumulate default values from parent declarations. `apply_default_values()` then applies them to Blender sockets, silently skipping problematic values (e.g., BUNDLE sockets).

## Bundle Socket Bridging for 4-Component Types

**File**: `lib/graph_utils.py`

MaterialX supports Vector4 and Color4, but Blender's shader nodes don't have direct Vector4 sockets. The solution uses `NodeCombineBundle` / `NodeSeparateBundle` nodes with helper functions:
- `blender_to_vector4_bundle()` / `blender_from_vector4_bundle()`
- `blender_to_color4_bundle()` / `blender_from_color4_bundle()`

These appear in node implementations that handle 4-component types (`std_lib.py`, `open_pbr_surface.py`, `standard_surface.py`).

## Self-Generating Code Operator

**File**: `lib/util_operator.py`

The `PrintClass` operator (`node_tree.print_class`) inspects an active Blender node group and prints the corresponding `@register_materialx_node` decorated function. This is the tool contributors use to scaffold new node definitions — build the mapping visually in Blender, run the operator, copy the output into the appropriate `lib/` file.

## Blender Addon Registration Pattern

**File**: `__init__.py` and each module

Each module defines `register()` and `unregister()` functions. Top-level `__init__.py` calls them in dependency order:

```
register:     properties → ui → handle → util_operator → usd_io
unregister:   usd_io → util_operator → handle → ui → properties  (reversed)
```

## Conventions

- **Naming**: Classes use `PascalCase`; functions use `snake_case`; PropertyGroups prefixed with `PG_`; constants in `UPPER_SNAKE_CASE`
- **Logging**: Each module has `logger = logging.getLogger(__name__)`; root `__init__.py` sets all to `WARNING` level
- **Error handling**: Graceful degradation — `try/except` with `logging.warning` or early `return`; never crashes the addon on bad input
- **Node creation**: Always use `create_blender_node()` from `lib/graph_utils.py` rather than `tree.nodes.new()` directly — it handles naming, labeling, and position from MaterialX `xpos`/`ypos` attributes
