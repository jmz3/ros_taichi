#!/usr/bin/env python3
import sys
from .urdfpy import URDF


# class Robot(URDF):


filename = sys.argv[1]
robot = URDF.load(filename)
for l in robot.links:
    print(l.taichi)
robot.show()
