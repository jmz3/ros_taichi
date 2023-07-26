#!/usr/bin/env sh

# use python script to load urdf files
function tcs() {
    filename=$1
    python3 ~/Desktop/ros_taichi/parser/parser.py "$filename"
}
