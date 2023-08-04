import numpy as np
import parse_vtk as vtk


def list_faces(t):
    t = t.copy()
    np.sort(t, axis=1)
    numTets, _ = t.shape
    f = np.empty((4 * numTets, 4), dtype=int)
    for i in range(numTets):
        a = t[i, 0]
        b = t[i, 1]
        c = t[i, 2]
        d = t[i, 3]
        f[i, :] = np.array([i, a, b, c])
        f[i + numTets, :] = np.array([i, a, b, d])
        f[i + 2 * numTets, :] = np.array([i, a, c, d])
        f[i + 3 * numTets, :] = np.array([i, b, c, d])
    return f


def extract_unique_triangles(f):
    _, indxs, count = np.unique(
        f[:, 1:4], axis=0, return_index=True, return_counts=True
    )
    return f[indxs[count == 1]]


def reconstruct(faces):
    numFace, _ = faces.shape
    newFaces = np.zeros((numFace, 3), dtype=int)
    for i, face in enumerate(faces):
        vert = tets[face[0]]
        hasVert = [False] * 4
        for j in range(4):
            for k in range(1, 4):
                if face[k] == vert[j]:
                    hasVert[j] = True

        if hasVert[0] and hasVert[2] and hasVert[1]:
            newFaces[i] = np.array([vert[0], vert[2], vert[1]])

        elif hasVert[0] and hasVert[3] and hasVert[2]:
            newFaces[i] = np.array([vert[0], vert[3], vert[2]])

        elif hasVert[0] and hasVert[1] and hasVert[3]:
            newFaces[i] = np.array([vert[0], vert[1], vert[3]])

        elif hasVert[1] and hasVert[2] and hasVert[3]:
            newFaces[i] = np.array([vert[1], vert[2], vert[3]])
    return newFaces


def extract_surface(t):
    f = list_faces(t)
    np.savetxt("before_extract_faces.txt", f, fmt="%d", delimiter="\t")
    f = extract_unique_triangles(f)
    f = reconstruct(f)
    return f


tets = vtk.tet_np.copy()
surf_np = extract_surface(tets)
np.savetxt("after_extract_faces.txt", surf_np, fmt="%d", delimiter="\t")
