# -*- coding: utf-8 -*-
"""
Created on July 5 00:00:00 2019

@author: Oliver K. Ernst <oernst@ucsd.edu>
"""

bl_info = {
    "name": "MeshPy in Blender",
    "description": "Simple interface to MeshPy in Blender",
    "author": "Oliver K. Ernst",
    "version": (0,1,0),
    "blender": (2, 7, 8),
    "location": "View3D > Add > Mesh",
    "warning": "",
    "wiki_url" : "http://salk.edu",
    "license": "GPL v2",
    "category": "Mesh"}

# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------

if "bpy" in locals():
    print("Reloading MeshPy/TetGen")
    import imp
    imp.reload(run)
    imp.reload(gui)

else:
    print("Importing MeshPy/TetGen")
    from . import run
    from . import gui

# General import
import bpy
import sys
import os



def register():
    bpy.utils.register_module(__name__)

    bpy.types.Scene.meshpy_tetgen = bpy.props.PointerProperty(type=gui.MeshPyTetGenPropGroup)

    print("MeshPy/Tetgen registered")



def unregister():

    bpy.utils.unregister_module(__name__)

    print("MeshPy/TetGen unregistered")



if __name__ == '__main__':
    register()
