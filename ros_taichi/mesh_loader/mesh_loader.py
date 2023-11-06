import numpy as np
import taichi as ti
import trimesh as tm
from abc import ABC, abstractmethod
import os


class LoadMesh(ABC):
    """
    Abstract class for loading meshes

    Params:
    -----
        path (str): path to the mesh file

    Returns:
    --------
        mesh (trimesh): mesh object

    """

    def __init__(self, path):
        self.path = path
        self.mesh = None
        self.vertices = None
        self.faces = None
        self.normals = None

    @abstractmethod
    def load(self) -> tm.Trimesh:
        pass


class LoadSTL(LoadMesh):
    """
    Class for loading STL meshes

    Params:
    -----
        path (str): path to the mesh file

    Returns:
    --------
        mesh (trimesh): mesh object

    """

    def __init__(self, path):
        """
        Constructor for LoadSTL class, which loads STL meshes from the given path

        Params:
        -------
            path (str): path to the mesh file

        Returns:
        --------
            mesh (trimesh): mesh object
        """
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(cur_path, path)

        super().__init__(file_name)

    def load(self) -> tm.Trimesh:
        """
        Load the mesh from the given path

        Params:
        -------
            None

        Returns:
        --------
            mesh (trimesh): mesh object that contains vertices, faces, and normals
        """
        self.mesh = tm.load_mesh(self.path)
        return self.mesh

    def get_vertices(self) -> ti.Vector.field:
        src_vertices = np.asarray(self.mesh.vertices, dtype=np.float32)
        if src_vertices.shape[1] != 3:
            raise ValueError("The number of vertices should be 3.")

        self.vertices = ti.Vector.field(n=3, dtype=ti.f32, shape=src_vertices.shape[0])
        self.vertices.from_numpy(src_vertices)

        return self.vertices

    def get_faces(self) -> ti.Vector.field:
        src_faces = np.asarray(self.mesh.faces, dtype=np.int32)
        if src_faces.shape[1] != 3:
            raise ValueError("The number of faces should be 3.")

        self.faces = ti.Vector.field(n=3, dtype=ti.i32, shape=src_faces.shape[0])
        self.faces.from_numpy(src_faces)

        return self.faces

    def get_normal(self) -> ti.Vector.field:
        src_normals = np.asarray(self.mesh.vertex_normals, dtype=np.float32)
        if src_normals.shape[1] != 3:
            raise ValueError("The number of normals should be 3.")

        self.normals = ti.Vector.field(n=3, dtype=ti.f32, shape=src_normals.shape[0])
        self.normals.from_numpy(src_normals)

        return self.normals


if __name__ == "__main__":
    # Taichi variables

    # attach to logger so trimesh messages will be printed to console
    tm.util.attach_to_log()
    ti.init(arch=ti.cpu)

    # load a mesh
    cur_path = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(cur_path, "model/Bunny.stl")
    mesh = tm.load_mesh(file_name)

    src_vertices = np.asarray(mesh.vertices / 100, dtype=np.float32)
    src_faces = np.asarray(mesh.faces, dtype=np.int32)
    src_normals = np.asarray(mesh.vertex_normals, dtype=np.float32)

    assert src_vertices.shape[1] == 3
    assert src_faces.shape[1] == 3

    # Get the number of vertices and faces
    n_vertices = src_vertices.shape[0]
    n_faces = src_faces.shape[0]

    vertices = ti.Vector.field(n=3, dtype=ti.f32, shape=n_vertices)
    vertices.from_numpy(src_vertices)
    faces = ti.Vector.field(n=3, dtype=ti.i32, shape=n_faces)
    faces.from_numpy(src_faces)
    normals = ti.Vector.field(n=3, dtype=ti.f32, shape=n_faces)
    normals.from_numpy(src_normals)

    # for face in mesh.faces:
    #     for vertex in face:
    #         print(vertex) if vertex > n_vertices else None

    # Taichi GUI
    window = ti.ui.Window("Mesh Loader", res=(960, 960), vsync=True)
    gui = window.get_gui()
    canvas = window.get_canvas()
    canvas.set_background_color((1, 1, 1))
    scene = ti.ui.Scene()
    camera = ti.ui.Camera()
    camera = ti.ui.Camera()
    camera.position(-1, -2, 3)  # x, y, z
    camera.lookat(0, 0, 0)
    camera.up(0, 0, 1)
    scene.set_camera(camera)

    origin = [0.0, 0.0, 0.0]
    axis_length = 0.5
    x_axis = ti.Vector.field(3, dtype=float, shape=2)
    y_axis = ti.Vector.field(3, dtype=float, shape=2)
    z_axis = ti.Vector.field(3, dtype=float, shape=2)

    while window.running:
        camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.SPACE)
        scene.set_camera(camera)
        # scene.ambient_light((0.1, 0.1, 0.1))
        # scene.point_light(pos=[0.4, 0.4, 0.4], color=[0.8, 0.8, 0.8])

        camera.up(0, 0, 1)

        scene.lines(x_axis, color=(1, 0, 0), width=1)
        scene.lines(y_axis, color=(0, 1, 0), width=1)
        scene.lines(z_axis, color=(0, 0, 1), width=1)

        # scene.mesh(vertices=vertices)
        # scene.particles(vertices, radius=0.001, color=(1, 1, 1))
        scene.mesh(
            vertices=vertices,
            indices=faces,
            normals=normals,
            color=(0, 0, 0),
            show_wireframe=True,
        )
        canvas.scene(scene)
        window.show()
