#!/usr/bin/env python3
import sys
from urdfpy.urdfpy.urdf import URDF


# class Robot(URDF):


filename = sys.argv[1]
robot = URDF.load(filename)
for l in robot.links:
    if l.taichi is not None:
        print(l.taichi.bodytype.body_type)
for m in robot.materials:
    if m.taichi is not None:
        print(m.taichi.materialproperty.filename)
robot.show()
