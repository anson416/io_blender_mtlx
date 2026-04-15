# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import os
import subprocess

BLENDER_EXE = os.environ.get("BLENDER_EXE")


def main():
    if not BLENDER_EXE:
        raise RuntimeError("BLENDER_EXE environment variable not set")
    if not os.path.exists(BLENDER_EXE):
        raise RuntimeError(f"Blender executable not found at {BLENDER_EXE}")
    env = os.environ.copy()
    # Add paths to MaterialX libraries if needed
    # env['MATERIALX_SEARCH_PATH'] = ""
    # env['PXR_USDMTLX_PLUGIN_SEARCH_PATHS'] = ""
    env["BLENDER_SYSTEM_SCRIPTS"] = os.path.join(
        os.path.dirname(__file__), "bl_env"
    )
    subprocess.run([BLENDER_EXE, "--python-use-system-env"], env=env)


if __name__ == "__main__":
    main()
