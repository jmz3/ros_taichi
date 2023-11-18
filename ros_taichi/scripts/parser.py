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

def mesh_loading(file_name):
    file_name = "/Users/guanyunliu/Desktop/ros_taichi/ros_taichi/sample_urdf/data/ur5/" + file_name
    if ".stl" in file_name:
        mesh = LoadSTL(file_name)
    elif ".dae" in file_name:
        mesh = LoadDAE(file_name)

    vertices = mesh.get_vertices()
    faces = mesh.get_faces()
    normals = mesh.get_normals()

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
joints = list(robot.joint_map.keys())
print(joints)
joint1 = robot.joint_map.get(joints[9])
joint2 = robot.joint_map.get(joints[0])
print("Parent is ", joint2.parent)
print("Child is ", joint2.child)
print("Transformation is ", joint2.origin)
# print("Transformation type is ", type(joint2.origin))
# print(robot.link_map.keys())
# print("-----------------------------")
# print(robot.joint_map.keys())
# print("-----------------------------")
# Use Taichi Rendering to visualize the ur5 robot
tm.util.attach_to_log()
ti.init(arch=ti.cpu)

# Base
# attach to logger so trimesh messages will be printed to console
base_collision_mesh_filename = links[0].collisions[0].geometry.mesh.filename
# print(base_collision_mesh_filename)
v_base, f_base, n_base = mesh_loading(base_collision_mesh_filename)
shoulder_collision_mesh_filename = links[1].collisions[0].geometry.mesh.filename
v_shoulder, f_shoulder, n_shoulder = mesh_loading(shoulder_collision_mesh_filename)

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

transform_shoulder = ti.Matrix.field(4, 4 ,dtype=ti.f32, shape=(1, 1))
trans_base_shoulder = joint2.origin.reshape(1,1,4,4).astype(np.float32)
# trans1 = np.array([[1, 0, 0, 0.5],
#                    [0, 1, 0, 0],
#                    [0, 0, 1, 0],
#                    [0, 0, 0, 1]]).reshape(1,1,4,4).astype(np.float32)
transform_shoulder.from_numpy(trans_base_shoulder)
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
        # transforms=transform_base,
    )
    scene.mesh_instance(
        vertices=v_shoulder,
        indices=f_shoulder,
        normals=n_shoulder,
        color=(0, 0, 0),
        show_wireframe=True,
        transforms=transform_shoulder,
    )
    canvas.scene(scene)
    window.show()
