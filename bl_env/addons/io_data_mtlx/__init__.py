# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import logging

from . import material_properties, material_ui, materialx_handle, usd_io
from .lib import util_operator

bl_info = {
    "name": "io_data_mtlx",
    "description": "MaterialX import for Blender",
    "author": "Frieder Erdmann, Activision",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "location": "Properties > Material",
    "category": "Import-Export",
    "support": "COMMUNITY",
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logger.addHandler(logging.StreamHandler())


def register():
    material_properties.register()
    material_ui.register()
    materialx_handle.register()
    util_operator.register()
    usd_io.register()


def unregister():
    material_ui.unregister()
    material_properties.unregister()
    materialx_handle.unregister()
    util_operator.unregister()
    usd_io.unregister()
