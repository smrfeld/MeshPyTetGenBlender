import bpy, bmesh
from mathutils import Vector
import math

import collections

import numpy as np

import functools

import itertools

import os

# MeshPy
from meshpy.tet import MeshInfo, build, Options

# Time
import time



# Function to make a tetgen mesh
def make_tetgen_mesh(vert_list, face_list):

    # Make the tetgen mesh
    mesh_info = MeshInfo()

    # Points
    mesh_info.set_points(vert_list)

    # Faces
    mesh_info.set_facets(face_list)

    # --- TEMP ---
    '''
    # Make an object from the surface we are planning to tetrahedronalize
    mesh_new = bpy.data.meshes.new("pre_tet_mesh")
    mesh_new.from_pydata(vert_list,[],face_list)
    mesh_new.validate(verbose=False) # Important! and i dont know why
    mesh_new.update()
    obj_new = bpy.data.objects.new("pre_tet",mesh_new)
    context.scene.objects.link(obj_new)
    # return
    '''
    # --- FIN TEMP ---

    # Tetrahedralize
    # Options:
    # neighout = Write out neighbors
    # facesout = Write out faces
    # edgesout = Write out edges
    # regionattrib = Write out element_attributes = unique id for every tet in a distinct volume
    # nobisect = Dont alter surface
    print("> Starting TetGen")
    opts = Options(switches='pq', neighout = True, facesout = True, edgesout = True, regionattrib = True, verbose = True, docheck = True)
    mesh_built = build(mesh_info, options=opts)
    print("> Finished TetGen successfully")

    return mesh_built



# New object from MeshPy
def new_obj_meshpy(obj_name, mesh_built):

    mesh_new = bpy.data.meshes.new(obj_name+"_mesh")

    vert_list = list(mesh_built.points)

    edge_list = list(mesh_built.edges)

    face_list = list(mesh_built.faces)

    # Build the object
    mesh_new.from_pydata(vert_list,edge_list,face_list)

    # Update
    mesh_new.validate(verbose=False) # Important! and i dont know why
    mesh_new.update()

    # Object
    obj_new = bpy.data.objects.new(obj_name,mesh_new)

    # Something
    scene = bpy.context.scene
    scene.objects.link(obj_new)



def run_meshpy(context):

    print("> Running: run_meshpy")

    # Time
    t_st = []
    t_st.append(time.time())

    # Get the active object
    ob_list = context.selected_objects

    if len(ob_list) != 1:
        raise SystemError("Please select one (and only one) object")
    else:
        ob = ob_list[0]
        ob_name = ob.name

    # Get vert list
    vert_list = [tuple(item.co) for item in ob.data.vertices]

    # Make sure everything is selected
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Get face list
    face_list = [i.vertices for i in ob.data.polygons if i.select]

    # Make sure the main guy is not selected, but is the active object
    ob.select = False
    context.scene.objects.active = ob

    # Time
    t_st.append(time.time())
    print("> Got object vert, face list: " + str(t_st[-1]-t_st[-2]))

    ###
    # Mesh
    ###

    mesh_built = make_tetgen_mesh(vert_list=vert_list, face_list=face_list)

    # Time
    t_st.append(time.time())
    print("> Built the mesh: " + str(t_st[-1]-t_st[-2]))

    # Make it an object
    new_obj_meshpy(ob_name, mesh_built);

    # Time
    t_st.append(time.time())
    print("> Created object: " + str(t_st[-1]-t_st[-2]))

    print("> Finished: run_meshpy")
