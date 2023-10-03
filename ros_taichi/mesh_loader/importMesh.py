import numpy as np
import taichi as ti
import trimesh as tm


# ---------------------------------------------------------------------------- #
# Taichi layout


# Taichi kernels
@ti.kernel
def init():
    ti.static_print("init", src_vertices.shape, n_faces)
    for i in range(n_vertices):
        vertices[i] = ti.Vector([0.0, 0.0, 0.0])
    for i in range(n_faces):
        faces[i] = ti.Vector([-1, -1, -1])


@ti.kernel
def load_vertices():
    ti.static_print("load_vertices", src_vertices[1])
    for i in range(n_vertices):
        vertices[i] = ti.Vector(src_vertices[i, 0:3])


@ti.kernel
def load_faces():
    for i in range(n_faces):
        faces[i] = ti.Vector([1, 1, 1])


if __name__ == "__main__":
    # Taichi variables

    # attach to logger so trimesh messages will be printed to console
    tm.util.attach_to_log()
    ti.init(arch=ti.vulkan, debug=True)

    # load a mesh
    file_name = "model/Bunny.stl"
    mesh = tm.load_mesh(file_name)

    src_vertices = mesh.vertices
    src_faces = mesh.faces
    print("vertices: ", src_vertices.shape)
    print("faces: ", src_faces.shape)
    # mesh.show()
    n_vertices = src_vertices.shape[0]
    n_faces = src_faces.shape[0]
    vertices = ti.Vector.field(3, dtype=ti.f32, shape=n_vertices)
    faces = ti.Vector.field(3, dtype=ti.i32, shape=n_faces)

    # Taichi GUI
    window = ti.ui.Window("Mesh Loader", (512, 512), vsync=True)
    gui = window.get_gui()
    canvas = window.get_canvas()
    scene = ti.ui.Scene()
    camera = ti.ui.Camera()

    init()
    print("init done")
    load_vertices()
    load_faces()
    while window.running:
        scene.set_camera(camera)
        # scene.point_light(pos=[0.4, 0.4, 0.4], color=0xFFFFFF)
        scene.mesh(vertices=vertices)
        window.show()
