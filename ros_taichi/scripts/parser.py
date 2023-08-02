#!/usr/bin/env python3
import sys
# import ros_taichi.third_parties.urdfpy.urdfpy.URDF
# from ..third_parties.urdfpy.urdfpy import URDF
from .. import third_parties

filename = sys.argv[1]
robot = third_parties.URDF.load(filename)
for l in robot.links:
    if l.taichi is not None:
        print(l.taichi.bodytype.body_type)
for m in robot.materials:
    if m.taichi is not None:
        print(m.taichi.materialproperty.filename)
robot.show()
