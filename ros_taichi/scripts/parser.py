#!/usr/bin/env python3
import sys
# import ros_taichi.third_parties.urdfpy.urdfpy.URDF
# from ..third_parties.urdfpy.urdfpy import URDF
from .. import third_parties
import numpy as np
import taichi as ti
import trimesh as tm
from abc import ABC, abstractmethod
from ..mesh_loader.mesh_loader import LoadSTL
from ..mesh_loader.mesh_loader import LoadDAE

# def mesh_loading(file_name):
#     mesh = tm.load_mesh(file_name)
#     print(file_name)
#     # mesh.apply_transform(mesh.transformations.random_rotation_matrix())
#     # print(mesh.get_position_as_numpy())

#     # src_vertices = np.asarray(mesh.vertices / 100, dtype=np.float32)
#     src_vertices = np.asarray(mesh.vertices, dtype=np.float32)
#     src_faces = np.asarray(mesh.faces, dtype=np.int32)
#     src_normals = np.asarray(mesh.vertex_normals, dtype=np.float32)

#     assert src_vertices.shape[1] == 3
#     assert src_faces.shape[1] == 3

#     # Get the number of vertices and faces
#     n_vertices = src_vertices.shape[0]
#     n_faces = src_faces.shape[0]

#     vertices = ti.Vector.field(n=3, dtype=ti.f32, shape=n_vertices)
#     vertices.from_numpy(src_vertices)
#     faces = ti.Vector.field(n=3, dtype=ti.i32, shape=n_faces)
#     faces.from_numpy(src_faces)
#     normals = ti.Vector.field(n=3, dtype=ti.f32, shape=n_faces)
#     normals.from_numpy(src_normals)
#     return vertices, faces, normals

filename = sys.argv[1]
robot = third_parties.URDF.load(filename)
# Get all links
links = robot.links
for l in robot.links:
    if l.taichi is not None:
        print(l.taichi.bodytype.body_type)
for m in robot.materials:
    if m.taichi is not None:
        print(m.taichi.materialproperty.filename)
# robot.show()
print(robot.link_map)
# Use Taichi Rendering to visualize the ur5 robot
tm.util.attach_to_log()
ti.init(arch=ti.cpu)

# Base
# attach to logger so trimesh messages will be printed to console
base_collision_mesh_filename = links[0].collisions[0].geometry.mesh.filename
print(base_collision_mesh_filename)
mesh_model_base = LoadSTL("/Users/guanyunliu/Desktop/ros_taichi/ros_taichi/sample_urdf/data/ur5/"+base_collision_mesh_filename)
v_base = mesh_model_base.get_vertices()
f_base = mesh_model_base.get_faces()
n_base = mesh_model_base.get_normals()
base_collision_mesh_filename = links[1].collisions[0].geometry.mesh.filename
mesh_model_shoulder = LoadSTL("/Users/guanyunliu/Desktop/ros_taichi/ros_taichi/sample_urdf/data/ur5/"+base_collision_mesh_filename)
v_shoulder = mesh_model_shoulder.get_vertices()
f_shoulder = mesh_model_shoulder.get_faces()
n_shoulder = mesh_model_shoulder.get_normals()
# base_vertices, base_faces, base_normals = mesh_loading(base_collision_mesh_filename)
# base_vertices, base_faces, base_normals = mesh_loading("collision/base.stl")
# print(base_vertices)

# Taichi GUI
window = ti.ui.Window("Mesh Loader", res=(960, 960), vsync=True)
gui = window.get_gui()
canvas = window.get_canvas()
canvas.set_background_color((1, 1, 1))
scene = ti.ui.Scene()
camera = ti.ui.Camera()
camera = ti.ui.Camera()
camera.position(-1, -1, 1)  # x, y, z
camera.lookat(0, 0, 0)
camera.up(0, 0, 1)
scene.set_camera(camera)

origin = [5.0, 0.0, 8.0]
axis_length = 0.5
x_axis = ti.Vector.field(3, dtype=float, shape=2)
y_axis = ti.Vector.field(3, dtype=float, shape=2)
z_axis = ti.Vector.field(3, dtype=float, shape=2)


x_axis[0], x_axis[1] = origin, [axis_length, 0, 0]
y_axis[0], y_axis[1] = origin, [0, axis_length, 0]
z_axis[0], z_axis[1] = origin, [0, 0, axis_length]

transform_base = ti.Vector.field(1,dtype=ti.f32, shape=(4, 4))
trans1 = np.array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
transform_base.from_numpy(trans1)
print(transform_base)
while window.running:
    camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.SPACE)
    scene.set_camera(camera)
    # scene.ambient_light((0.1, 0.1, 0.1))
    # scene.point_light(pos=[0.4, 0.4, 0.4], color=[0.8, 0.8, 0.8])

    scene.lines(x_axis, color=(1, 0, 0), width=6)
    scene.lines(y_axis, color=(0, 1, 0), width=6)
    scene.lines(z_axis, color=(0, 0, 1), width=6)

    # scene.mesh(vertices=vertices)
    # scene.particles(vertices, radius=0.001, color=(1, 1, 1))
    scene.mesh_instance(
        vertices=v_base,
        indices=f_base,
        normals=n_base,
        color=(0, 0, 0),
        show_wireframe=True,
        # transforms(),
    )
    canvas.scene(scene)
    window.show()
