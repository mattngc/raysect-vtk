from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import sys
import numpy
import os
import os.path as path
import multiprocessing

threads = multiprocessing.cpu_count()
force = False
profile = False

if "--force" in sys.argv:
    force = True
    del sys.argv[sys.argv.index("--force")]

if "--profile" in sys.argv:
    profile = True
    del sys.argv[sys.argv.index("--profile")]

compilation_includes = [".", numpy.get_include()]

setup_path = path.dirname(path.abspath(__file__))

# build extension list
extensions = []
for root, dirs, files in os.walk(setup_path):
    for file in files:
        if path.splitext(file)[1] == ".pyx":
            pyx_file = path.relpath(path.join(root, file), setup_path)
            module = path.splitext(pyx_file)[0].replace("/", ".")
            extensions.append(Extension(module, [pyx_file], include_dirs=compilation_includes),)

if profile:
    directives = {"profile": True}
else:
    directives = {}


setup(
    name="raysect-vtk",
    version="0.5.0",
    url="http://www.raysect.org",
    author="Dr Matthew Carr et al.",
    author_email="developers@raysect.org",
    description='Visualisation tools with VTK for the Raysect ray-tracing framework',
    license="BSD",
    # namespace_packages=['raysect'],
    packages=find_packages(),
    include_package_data=True,
    ext_modules=cythonize(extensions, nthreads=threads, force=force, compiler_directives=directives)
)