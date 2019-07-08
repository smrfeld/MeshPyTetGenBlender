import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy.app.handlers import persistent
import mathutils
from bpy_extras.io_utils import ImportHelper

# Run MeshPy
from . import run
from . import export_to_xml

import os

# Register
def register():
    bpy.utils.register_module(__name__)

# Unregister
def unregister():
    bpy.utils.unregister_module(__name__)

# Main panel class
class MeshPyTetGenVizPanel(bpy.types.Panel):
    bl_label = "Interface to MeshPy/TetGen" # Panel name
    bl_space_type = "VIEW_3D" # where to put panel
    bl_region_type = "TOOLS" # sub location
    bl_category = "MeshPy/Tetgen interface"

    @classmethod
    def poll(cls, context):
        return (context.scene is not None)

    def draw(self, context):
        context.scene.meshpy_tetgen.draw ( self.layout )

#######################################################
#######################################################
# Tet object list
#######################################################
#######################################################

class VertexObj(bpy.types.PropertyGroup):
    x = FloatProperty( default = 0.0 )
    y = FloatProperty( default = 0.0 )
    z = FloatProperty( default = 0.0 )

    def set_from_list(self, arr):
        self.x = arr[0]
        self.y = arr[1]
        self.z = arr[2]

    def get_list(self):
        return [self.x,self.y,self.z]

class TetObj(bpy.types.PropertyGroup):
    v0 = IntProperty( default = 0 )
    v1 = IntProperty( default = 0 )
    v2 = IntProperty( default = 0 )
    v3 = IntProperty( default = 0 )

    def set_from_list(self, arr):
        self.v0 = arr[0]
        self.v1 = arr[1]
        self.v2 = arr[2]
        self.v3 = arr[3]

    def get_list(self):
        return [self.v0,self.v1,self.v2,self.v3]

# Class to hold the object
class MeshPyTetGenObject(bpy.types.PropertyGroup):
    name = StringProperty ( name="Name", default="", description="Object Name" )
    vert_list = CollectionProperty(type=VertexObj, name = "Vertex list")
    tet_list = CollectionProperty(type=TetObj, name = "Tet list")

    # Draw in list of objects
    def draw_item_in_row ( self, row ):
        col = row.column()
        col.label ( str(self.name) )

# Model object item to draw in the list
class MeshPyTetGen_UL_object(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # The item will be a MeshPyTetGenMeshObject
        # Let it draw itself in a new row:
        item.draw_item_in_row ( layout.row() )

# Button to remove model object
class MeshPyTetGenObjectRemove(bpy.types.Operator):
    bl_idname = "meshpy_tetgen.mesh_object_remove"
    bl_label = "Remove a Mesh Object"
    bl_description = "Remove a mesh object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.meshpy_tetgen.remove_mesh_object()
        return {'FINISHED'}

# Button to remove all model objects
class MeshPyTetGenObjectRemoveAll(bpy.types.Operator):
    bl_idname = "meshpy_tetgen.mesh_object_remove_all"
    bl_label = "Remove all Mesh Objects"
    bl_description = "Remove all mesh objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.meshpy_tetgen.remove_all_mesh_objects()
        return {'FINISHED'}

#######################################################
#######################################################
# Classes
#######################################################
#######################################################

class RunMeshPyTetGen(bpy.types.Operator):
    bl_idname = "meshpy_tetgen.run"
    bl_label = "Run MeshPy/TetGen"

    def execute ( self, context ):
        success, new_obj, meshpy_obj = run.run(context)

        # If successful, add the object to the list
        if success:
            context.scene.meshpy_tetgen.add_mesh_object(new_obj.name, meshpy_obj)

        return {"FINISHED"}

class ExportToXML(bpy.types.Operator):
    bl_idname = "meshpy_tetgen.export_to_xml"
    bl_label = "Export to DOLFIN XML format"

    def execute ( self, context ):

        # Get the filename
        s = context.scene.meshpy_tetgen
        fname = s.filename
        obj = s.mesh_obj_list[s.active_object_index]
        vert_list = [pt.get_list() for pt in obj.vert_list]
        tet_list = [tet.get_list() for tet in obj.tet_list]

        export_to_xml.export_to_xml(fname,vert_list,tet_list)

        return {"FINISHED"}

class SetFilename(bpy.types.Operator, ImportHelper):
    bl_idname = "meshpy_tetgen.set_filename"
    bl_label = "Set filename"

    filepath = bpy.props.StringProperty(subtype='FILE_PATH', default="")

    filename_ext = ".xml" # allowed extensions

    # Get the filename
    def execute(self, context):

        # store
        if self.filepath[-4:] != self.filename_ext:
            raise SystemError("Must be: " + str(self.filename_ext) + " format but you chose: " + str(self.filepath[-4:]) + "!")
        else:
            context.scene.meshpy_tetgen.filename = self.filepath

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#######################################################
#######################################################
# Main GUI property group
#######################################################
#######################################################

# Class for context that contains all the functions
class MeshPyTetGenPropGroup(bpy.types.PropertyGroup):

    # List of mesh objects
    mesh_obj_list = CollectionProperty(type=MeshPyTetGenObject, name="Mesh List")
    active_object_index = IntProperty(name="Active Object Index", default=0)

    # Filename
    filename = StringProperty( default="~/mesh.xml" )

    # Draw
    def draw(self,layout):

        box = layout.box()
        row = box.row(align=True)
        row.alignment = 'LEFT'

        row = box.row()
        row.label("Interface to MeshPy/TetGen", icon='SURFACE_DATA')

        row = box.row()
        col = row.column()

        col.template_list("MeshPyTetGen_UL_object", "",
                          self, "mesh_obj_list",
                          self, "active_object_index",
                          rows=2)

        col = row.column(align=True)
        col.operator("meshpy_tetgen.mesh_object_remove", icon='ZOOMOUT', text="")
        col.operator("meshpy_tetgen.mesh_object_remove_all", icon='X', text="")

        row = box.row()
        row.label("Run MeshPy/TetGen on the selected object")
        row.operator("meshpy_tetgen.run")

        row = box.row()
        row.label("Export to DOLFIN XML format")
        row = box.row()
        row.operator("meshpy_tetgen.set_filename")
        row.label(self.filename)
        row = box.row()
        row.operator("meshpy_tetgen.export_to_xml")

    # Add a mesh object to the list
    def add_mesh_object(self, name, meshpy_object):
        print("Adding mesh object to the list")

        # Check by name if the object already is in the list
        current_object_names = [d.name for d in self.mesh_obj_list]
        if not name in current_object_names:
            obj = self.mesh_obj_list.add()
        else:
            idx = current_object_names.index(name)
            obj = self.mesh_obj_list[idx]

            # Clear vert list, tet list
            while len(obj.vert_list) > 0:
                obj.vert_list.remove ( 0 )
            while len(obj.tet_list) > 0:
                obj.tet_list.remove ( 0 )

        obj.name = name
        for i in range(0,len(meshpy_object.points)):
            obj.vert_list.add()
            obj.vert_list[i].set_from_list(meshpy_object.points[i])
        for i in range(0,len(meshpy_object.elements)):
            obj.tet_list.add()
            obj.tet_list[i].set_from_list(meshpy_object.elements[i])

    # Remove a mesh object
    def remove_mesh_object(self):
        print("Removing mesh object from the list")

        self.mesh_obj_list.remove ( self.active_object_index )
        if self.active_object_index > 0:
            self.active_object_index -= 1

    # Remove all mesh objects
    def remove_all_mesh_objects(self):
        print("Removing all mesh objects")

        while len(self.mesh_obj_list) > 0:
            self.mesh_obj_list.remove ( 0 )
        self.active_object_index = 0
