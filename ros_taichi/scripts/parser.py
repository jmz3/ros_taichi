#!/usr/bin/env python3
import sys
# import ros_taichi.third_parties.urdfpy.urdfpy.URDF
# from ..third_parties.urdfpy.urdfpy import URDF
from .. import third_parties
import numpy as np
import taichi as ti
import trimesh as tm
from abc import ABC, abstractmethod
from ..mesh_loader import mesh_loader

def mesh_loading(file_name):
    mesh = tm.load_mesh(file_name)
    print(file_name)
    # mesh.apply_transform(mesh.transformations.random_rotation_matrix())
    # print(mesh.get_position_as_numpy())

    # src_vertices = np.asarray(mesh.vertices / 100, dtype=np.float32)
    src_vertices = np.asarray(mesh.vertices, dtype=np.float32)
    src_faces = np.asarray(mesh.faces, dtype=np.int32)
    src_normals = np.asarray(mesh.vertex_normals, dtype=np.float32)

    assert src_vertices.shape[1] == 3
    assert src_faces.shape[1] == 3

    # Get the number of vertices and faces
    n_vertices = src_vertices.shape[0]
    n_faces = src_faces.shape[0]

    vertices = ti.Vector.field(n=3, dtype=ti.f32, shape=n_vertices)
    vertices.from_numpy(src_vertices)
    faces = ti.Vector.field(n=3, dtype=ti.i32, shape=n_faces)
    faces.from_numpy(src_faces)
    normals = ti.Vector.field(n=3, dtype=ti.f32, shape=n_faces)
    normals.from_numpy(src_normals)
    return vertices, faces, normals

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
base_collision_mesh_filename = links[3].collisions[0].geometry.mesh.filename
base_vertices, base_faces, base_normals = mesh_loading(base_collision_mesh_filename)
# base_vertices, base_faces, base_normals = mesh_loading("collision/base.stl")
# print(base_vertices)

# i = 1
# for l in links:
#     print("link No ", i)
#     if l is not None:
#         print("Not None")
#         # mesh_base = l.visuals[0]
#         # print(l.visuals)
#     else:
#         print("None")
#     i += 1


# Taichi GUI
window = ti.ui.Window("Mesh Loader", res=(960, 960), vsync=True)
gui = window.get_gui()
canvas = window.get_canvas()
canvas.set_background_color((1, 1, 1))
scene = ti.ui.Scene()
camera = ti.ui.Camera()
camera = ti.ui.Camera()
camera.position(-1, -2, 3)  # x, y, z
camera.lookat(0, 0, 0)
camera.up(0, 0, 1)
scene.set_camera(camera)

origin = [5.0, 0.0, 8.0]
axis_length = 0.5
x_axis = ti.Vector.field(3, dtype=float, shape=2)
y_axis = ti.Vector.field(3, dtype=float, shape=2)
z_axis = ti.Vector.field(3, dtype=float, shape=2)

while window.running:
    camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.SPACE)
    scene.set_camera(camera)
    # scene.ambient_light((0.1, 0.1, 0.1))
    # scene.point_light(pos=[0.4, 0.4, 0.4], color=[0.8, 0.8, 0.8])

    camera.up(0, 0, 1)

    scene.lines(x_axis, color=(1, 0, 0), width=6)
    scene.lines(y_axis, color=(0, 1, 0), width=6)
    scene.lines(z_axis, color=(0, 0, 1), width=6)

    # scene.mesh(vertices=vertices)
    # scene.particles(vertices, radius=0.001, color=(1, 1, 1))
    scene.mesh(
        vertices=base_vertices,
        indices=base_faces,
        normals=base_normals,
        color=(0, 0, 0),
        show_wireframe=True,
    )
    canvas.scene(scene)
    window.show()
