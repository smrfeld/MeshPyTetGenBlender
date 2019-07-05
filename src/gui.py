import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy.app.handlers import persistent
import mathutils
from bpy_extras.io_utils import ImportHelper

# Run MeshPy
from . import run_meshpy

import os

# Register
def register():
    bpy.utils.register_module(__name__)

# Unregister
def unregister():
    bpy.utils.unregister_module(__name__)

# Main panel class
class MeshPyBlenderVizPanel(bpy.types.Panel):
    bl_label = "MeshPy interface" # Panel name
    bl_space_type = "VIEW_3D" # where to put panel
    bl_region_type = "TOOLS" # sub location
    bl_category = "MeshPy Blender"

    @classmethod
    def poll(cls, context):
        return (context.scene is not None)

    def draw(self, context):
        context.scene.meshpy_blender.draw ( self.layout )

#######################################################
#######################################################
# Classes to run MeshPy
#######################################################
#######################################################

# Class to close open caps
class RunMeshpy(bpy.types.Operator):
    bl_idname = "meshpy_blender.run_meshpy"
    bl_label = "Run MeshPy"

    def execute ( self, context ):
        print ( "Run MeshPy" )
        run_meshpy.run_meshpy(context)
        return {"FINISHED"}

#######################################################
#######################################################
# Main GUI property group
#######################################################
#######################################################

# Class for context that contains all the functions
class MeshPyBlenderPropGroup(bpy.types.PropertyGroup):

    # Draw
    def draw(self,layout):

        box = layout.box()
        row = box.row(align=True)
        row.alignment = 'LEFT'

        row = box.row()
        row.label("Tools for the MCell surface mesh", icon='SURFACE_DATA')

        row = box.row()
        split = box.split()
        col = split.column(align=True)
        col.label("Run MeshPy")
        col.operator("meshpy_blender.run_meshpy")
