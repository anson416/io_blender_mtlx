# io_blender_mtlx

Blender addon for loading and displaying MaterialX materials. Converts MaterialX documents into native Blender shader node groups, with editable inputs exposed as Material properties. Generated node graphs work without the addon active.

**Requires Blender 5.0+** (needs node bundles feature).

## Tech Stack

- **Language**: Python 3.11 (pinned in `.python-version`)
- **Package manager**: [uv](https://docs.astral.sh/uv/) (`pyproject.toml`, `uv.lock`)
- **Dependencies**: `materialx>=1.39.4` (for XML parsing), `fake-bpy-module-latest` (Blender API stubs for IDE)
- **Dev launch**: `launch_blender.py` (sets `BLENDER_SYSTEM_SCRIPTS` to `bl_env/` and launches Blender)

## Key Directories

| Path | Purpose |
|---|---|
| `bl_env/addons/io_data_mtlx/` | Addon source (entry point, core logic, UI) |
| `bl_env/addons/io_data_mtlx/lib/` | Node mapping implementations and utilities |
| `examples/` | Sample `.mtlx` files |

## Essential Commands

```bash
uv sync --dev          # Install deps (including fake-bpy-module)
BLENDER_EXE=/path/to/blender python launch_blender.py  # Launch Blender with addon
```

No tests, linters, or CI are configured.

## Architecture Overview

1. User picks a `.mtlx` file on a Blender Material → `materialx_handle.py:MaterialXHandle.load_document()`
2. Inputs extracted and synced to `Material.mtlx_inputs` collection (`material_properties.py`)
3. Document flattened (`material_flatten.py`) to resolve NodeGraphs into a single-level graph
4. Node graph generated (`material_generate.py`) via two-pass: create nodes → wire connections
5. Each MaterialX node type is mapped by a registered function in `lib/` (decorator-based registry, `lib/node_registry.py`)
6. On USD export, `usd_io.py:USDMTLXRefHook` embeds MTLX references and attribute values

## Additional Documentation

When working on specific aspects, check these files for detailed patterns:

- [Architectural Patterns](.claude/docs/architectural_patterns.md) — Node registry, PropertyGroup data model, type mapping, graph generation, code generation operator, conventions
- [README.md](README.md) — Workflow description, supported nodes, contribution guidelines, technical architecture diagram
