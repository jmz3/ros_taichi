import numpy as np
import taichi as ti
import trimesh as tm


# ---------------------------------------------------------------------------- #
# Taichi layout


# Taichi kernels
@ti.kernel
def init():
    for i in range(n_vertices):
        vertices[i] = ti.Vector([0.0, 0.0, 0.0])
    for i in range(n_faces):
        faces[i] = ti.Vector([-1, -1, -1])


@ti.kernel
def load_vertices():
    for i in range(n_vertices):
        vertices[i] = ti.Vector(
            [mesh.vertices[i][0], mesh.vertices[i][1], mesh.vertices[i][2]]
        )


@ti.kernel
def load_faces():
    for i in range(n_faces):
        faces[i] = ti.Vector([mesh.faces[i][0], mesh.faces[i][1], mesh.faces[i][2]])


if __name__ == "__main__":
    # Taichi variables

    # attach to logger so trimesh messages will be printed to console
    tm.util.attach_to_log()

    # load a mesh
    file_name = "model/Bunny.stl"
    mesh = tm.load_mesh(file_name)

    vertices = mesh.vertices
    faces = mesh.faces
    print("vertices: ", vertices.shape)
    print("faces: ", faces.shape)
    # mesh.show()
    n_vertices = vertices.shape[0]
    n_faces = faces.shape[0]
    vertices = ti.Vector.field(3, dtype=ti.f32, shape=n_vertices)
    faces = ti.Vector.field(3, dtype=ti.i32, shape=n_faces)

    # Taichi GUI
    gui = ti.GUI("Taichi", (512, 512))
    init()
    load_vertices()
    load_faces()
    while gui.running:
        gui.get_event()
        gui.clear(0x112F41)
        gui.show()
