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
        # print(mesh)
    elif ".dae" in file_name:
        mesh = LoadDAE(file_name)

    vertices = mesh.get_vertices()
    faces = mesh.get_faces()
    normals = mesh.get_normals()

    return vertices, faces, normals

def set_pose(urdf_robot, desired_angles):
    # This function is for UR5 only
    # TODO: Need to come up with a general version
    idx = 0
    for j in urdf_robot.joints:
        new_config = j.get_child_pose(desired_angles[idx])
        j.origin = new_config
        idx += 1
        if idx > 5:
            break
        # if j.is_valid(new_config):
        #     j.origin = new_config
        #     idx += 1
        # else:
        #     print("Non-valid Configuration!")



filename = sys.argv[1]
robot = third_parties.URDF.load(filename)
# Get all links
links = robot.links
joints = robot.joints
joints_map = robot.joint_map

angle = np.array([0, -np.pi/3, np.pi/2, -2*np.pi/3, -np.pi/2, 0])
set_pose(robot, angle)
# angle = [0,0,0,0,np.pi/2,0]
# print(joints_map)
# origin_new = joints[1].get_child_pose(angle)
# print(joints[1].get_child_pose(angle))
# joints[1].origin = origin_new
# for j in robot.jonits:

# for l in robot.links:
#     if l.taichi is not None:
#         print(l.taichi.bodytype.body_type)
# for m in robot.materials:
#     if m.taichi is not None:
#         print(m.taichi.materialproperty.filename)
# robot.show()
robot.showTemp(use_collision=True)
