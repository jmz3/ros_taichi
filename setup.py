#!/usr/bin/env python3

from setuptools import setup

requirements = [
    'lxml',             # For XML DOM Tree
    'networkx==3.1',    # For joint graph
    'numpy',            # Numpy
    'pillow',           # For texture image loading
    'pycollada==0.6',   # COLLADA (.dae) mesh loading via trimesh
    'pyrender>=0.1.20', # For visualization
    'scipy',            # For trimesh, annoyingly
    'six',              # Python 2/3 compatability
    'trimesh',          # Mesh geometry loading/creation/saving
]

dev_requirements = [
    'flake8',            # Code formatting checker
    'pre-commit',        # Pre-commit hooks
    'pytest',            # Code testing
    'pytest-cov',        # Coverage testing
    'tox',               # Automatic virtualenv testing
]

docs_requirements = [
    'sphinx',            # General doc library
    'sphinx_rtd_theme',  # RTD theme for sphinx
    'sphinx-automodapi'  # For generating nice tables
]

setup(
    name='ros_taichi',
    version='0.1',
    description='An interface allows ROS users to run simulation on Taichi',
    long_description='some text here!',
    author='Jeremy Zhang, Guanyun Liu',
    author_email='sample@email.com',
    license='MIT License',
    # url='https://github.com/jmz3/ros_taichi',
    keywords='robotics ros taichi soft rigid simulation',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering'
    ],
    packages=['ros_taichi'],
    setup_requires = requirements,
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
        'docs': docs_requirements,
    }
)
