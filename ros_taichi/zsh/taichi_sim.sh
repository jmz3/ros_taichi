#!/usr/bin/env sh

# use python script to load urdf files
function tcs() {
    filename=$1
    # python3 -m ~/Desktop/ros_taichi/ros_taichi/scripts/parser.py "$filename"
    python3 -m ros_taichi.scripts.parser "$filename"
    # python3 ~/Desktop/ros_taichi/ros_taichi/parser.py "$filename"
}
