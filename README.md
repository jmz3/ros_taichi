# ros_taichi
ROS-Taichi Integration for High Performance Physics Simulation

## Installation
### macos
1. Clone the git repository

``` sh
git clone https://github.com/jmz3/ros_taichi.git
```
(Optional) You can use the `--recurse-submodules` to download the `urdfpy` submodule together with the `ros_taichi` repository.

``` sh
git clone https://github.com/jmz3/ros_taichi.git --recurse-submodules
```
Or, if you clone the repository without using the `--recurse-submodules` flag, you can use the following command to download the submodule.

``` sh
cd <root/of/ros_taichi/directory>
git submodule update
```
2. Install the `ros_taichi` package

``` sh
pip install -e <path/to/your/ros_taichi/root/directory>
```
e.g.

``` sh
pip install -e $Home/Desktop/ros_taichi
```
Note: make sure you activate your virtual environment before using pip install. Double check the pip path. For example, if you are using `mambaforge`, then the pip path could be `<path/to/your/mambaforge>/envs/ros_env/bin/pip`.

## Example
To run the parser example, go to the `sample_urdf` directory and then run

``` sh
python -m ros_taichi.scripts.parser robot.urdf
```

# Using Trimesh for loading meshes
## Installation
For minial installation, you can use the following command to install `trimesh`:
``` sh
pip install trimesh
```
