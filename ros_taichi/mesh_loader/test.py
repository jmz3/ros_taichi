from mesh_loader import LoadSTL
import taichi as ti

if __name__ == "__main__":
    ti.init(arch=ti.cpu)

    stl = LoadSTL("model/Bunny.stl")

    v = stl.get_vertices()
    print(v.shape)
