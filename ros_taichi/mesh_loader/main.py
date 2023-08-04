import taichi as ti
import taichi.math as tm
import numpy as np
import parse_vtk as vtk
import extract_surf

ti.init()

# import data from the parsed vtk, save as numpy array
pos_np = vtk.pos_np
tet_np = vtk.tet_np
numParticles, _ = pos_np.shape
numTets, _ = tet_np.shape


# copy data from extract_surf
surf_np = extract_surf.surf_np
numSurfs, _ = surf_np.shape

# copy data to the taichi field
pos = ti.Vector.field(3, float, numParticles)
tet = ti.Vector.field(4, int, numTets)
surf = ti.Vector.field(3, int, numSurfs)
pos.from_numpy(pos_np)
tet.from_numpy(tet_np)
surf.from_numpy(surf_np)
# ---------------------------------------------------------------------------- #
#                                      gui                                     #
# ---------------------------------------------------------------------------- #
surf_show = ti.field(int, numSurfs * 3)
surf_show.from_numpy(surf_np.flatten())

# init the window, canvas, scene and camerea
window = ti.ui.Window("parse_vtk", (1024, 1024), vsync=True)
canvas = window.get_canvas()
scene = ti.ui.Scene()
camera = ti.ui.make_camera()

# initial camera position
camera.position(0.5, 1.0, 1.95)
camera.lookat(0.5, 0.3, 0.5)
camera.fov(55)


@ti.kernel
def init_pos():
    for i in range(numParticles):
        pos[i] /= 100.0  # data is too large, so scale it
        pos[i] += tm.vec3(0.5, 1, 0)


def main():
    init_pos()
    np.savetxt("surf.csv", surf_np, fmt="%d", delimiter="\t")
    while window.running:
        # set the camera, you can move around by pressing 'wasdeq'
        camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.RMB)
        scene.set_camera(camera)

        # set the light
        scene.point_light(pos=(0, 1, 2), color=(1, 1, 1))
        scene.point_light(pos=(0.5, 1.5, 0.5), color=(0.5, 0.5, 0.5))
        scene.ambient_light((0.5, 0.5, 0.5))

        # draw
        # scene.particles(pos, radius=0.02, color=(0, 1, 1))
        scene.mesh(pos, indices=surf_show)

        # show the frame
        canvas.scene(scene)
        window.show()


if __name__ == "__main__":
    main()
