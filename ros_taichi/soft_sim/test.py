import taichi as ti
from ros_taichi.mesh_loader.mesh_loader import LoadSTL, LoadDAE

# Initialize Taichi
ti.init(arch=ti.vulkan)

# Constants

ground_height = 0.0
elasticity = 0.5  # Adjust the elasticity of the mesh
damping = 0.05  # Damping factor

# Load your mesh
mesh_model = LoadSTL("../mesh_loader/model/forearm.stl")  # Load STL model

num_vertices = mesh_model.vertices.shape[0]
num_faces = mesh_model.faces.shape[0]
num_normals = mesh_model.normals.shape[0]

# Fields
vertices = ti.Vector.field(3, dtype=ti.float32, shape=num_vertices)
velocity = ti.Vector.field(3, dtype=ti.float32, shape=num_vertices)
faces = ti.Vector.field(3, dtype=ti.int32, shape=num_faces)  # Assuming triangular faces

# Gravity
gravity = ti.Vector([0, -9.81, 0])


@ti.kernel
def apply_gravity(dt: ti.f32):
    for i in vertices:
        # Apply gravity
        velocity[i] += gravity * dt
        # Simple Euler integration to update positions
        vertices[i] += velocity[i] * dt
        # Collision with ground
        if vertices[i].y < ground_height:
            # Simple collision response
            vertices[i].y = ground_height
            velocity[i].y *= -elasticity
            # Damping
            velocity[i] *= 1 - damping


def initialize_mesh():
    # Initialize vertices
    vertices = mesh_model.get_vertices()
    # Initialize faces
    faces = mesh_model.get_faces()

    for i in range(num_vertices):
        vertices[i] += [0.5, 0.5, 0.5]
        velocity[i] = [0, 0, 0]


def main():
    initialize_mesh()
    window = ti.ui.Window("Mesh Deformation", (800, 800))
    canvas = window.get_canvas()
    canvas.set_background_color((1, 1, 1))
    scene = ti.ui.Scene()
    camera = ti.ui.Camera()
    camera.position(-1, -1, 1)  # x, y, z
    camera.lookat(0, 0, 0)
    camera.up(0, 0, 1)
    scene.set_camera(camera)

    while window.running:
        apply_gravity(0.01)
        # Render your mesh
        # This can be as simple as drawing lines between vertices or more complex rendering

        # scene.set_camera(camera)

        scene.particles(vertices, radius=0.01, color=(1, 1, 1))
        print(vertices[0])
        canvas.scene(scene)
        window.show()


if __name__ == "__main__":
    main()
