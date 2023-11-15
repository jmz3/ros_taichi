from mesh_loader import LoadSTL
from mesh_loader import LoadDAE
import taichi as ti
import trimesh as tm

if __name__ == "__main__":
    # ti.init(arch=ti.cpu)

    # mesh_model = LoadSTL("model/Bunny.stl") # Load STL model
    # mesh_model = LoadDAE("model/forearm.dae")  # Load DAE model

    # load dae model to trimesh

    # Load the DAE file
    mesh = tm.load("model/forearm.dae")

    # Access mesh information

    mesh.show()

    for mesh in mesh.geometry.values():
        print(mesh)
        print(mesh.vertices.shape)
        print(mesh.faces.shape)
        print(mesh.vertex_normals.shape)
    # print(faces)
    # print(normals)

# Do further processing or visualization with the loaded mesh


# v = mesh_model.get_vertices()
# f = mesh_model.get_faces()
# n = mesh_model.get_normals()

# window = ti.ui.Window("Mesh Loader", res=(960, 960), vsync=True)
# gui = window.get_gui()
# canvas = window.get_canvas()
# canvas.set_background_color((1, 1, 1))
# scene = ti.ui.Scene()
# camera = ti.ui.Camera()
# camera = ti.ui.Camera()
# camera.position(-1, -1, 1)  # x, y, z
# camera.lookat(0, 0, 0)
# camera.up(0, 0, 1)
# scene.set_camera(camera)

# origin = [0.0, 0.0, 0.0]
# axis_length = 0.5
# x_axis = ti.Vector.field(3, dtype=float, shape=2)
# y_axis = ti.Vector.field(3, dtype=float, shape=2)
# z_axis = ti.Vector.field(3, dtype=float, shape=2)

# x_axis[0], x_axis[1] = origin, [axis_length, 0, 0]
# y_axis[0], y_axis[1] = origin, [0, axis_length, 0]
# z_axis[0], z_axis[1] = origin, [0, 0, axis_length]

# while window.running:
#     camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.SPACE)
#     scene.set_camera(camera)

#     scene.lines(x_axis, color=(1, 0, 0), width=1)
#     scene.lines(y_axis, color=(0, 1, 0), width=1)
#     scene.lines(z_axis, color=(0, 0, 1), width=1)

#     # scene.mesh(vertices=vertices)
#     # scene.particles(vertices, radius=0.001, color=(1, 1, 1))
#     scene.mesh(
#         vertices=v,
#         indices=f,
#         normals=n,
#         color=(0, 0, 0),
#         show_wireframe=True,
#     )
#     canvas.scene(scene)
#     window.show()
