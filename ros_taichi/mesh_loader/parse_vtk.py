fileName = "model/Armadillo13K.vtk"
pos = []
tet = []

import re


def read_vtk(fileName, pos, tet):
    isVert = False
    isTet = False
    with open(fileName, "r") as f:
        for line in f.readlines():
            if re.match("POINTS", line):
                line = line.split()
                isVert = True
                numVerts = line[1]
                print(f"read {numVerts} verts")
                continue
            elif re.match("CELLS", line):
                line = line.split()
                isTet = True
                isVert = False
                numTets = line[1]
                print(f"read {numTets} tets")
                continue
            elif line == "\n":
                continue
            elif re.match("CELL_TYPES", line):
                break

            if isVert:
                line = line.split()
                pos.append([line[0], line[1], line[2]])
            if isTet:
                line = line.split()
                tet.append([line[1], line[2], line[3], line[4]])


read_vtk(fileName, pos, tet)

# copy data to numpy
import numpy as np

pos_np = np.array(pos, dtype=float).reshape((-1, 3))
tet_np = np.array(tet, dtype=int).reshape((-1, 4))
