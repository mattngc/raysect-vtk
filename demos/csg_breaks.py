
from matplotlib.pyplot import *
from numpy import array

from raysect.primitive import Sphere, Box, Cylinder, Union, Intersect, Subtract
from raysect.optical import World, translate, rotate, Point3D, d65_white, InterpolatedSF
from raysect.optical.material.emitter import UniformSurfaceEmitter, Checkerboard
from raysect.optical.material.dielectric import Dielectric, Sellmeier
from raysect.optical.library import schott
from raysect.optical.observer import PinholeCamera, RGBPipeline2D, SpectralPowerPipeline2D

world = World()

cyl_x = Cylinder(1, 4.2, transform=rotate(90, 0, 0)*translate(0, 0, -2.1))
cyl_y = Cylinder(1, 4.2, transform=rotate(0, 90, 0)*translate(0, 0, -2.1))
cyl_z = Cylinder(1, 4.2, transform=rotate(0, 0, 0)*translate(0, 0, -2.1))

# Intersect(sphere, Subtract(cube, Union(Union(cyl_x, cyl_y), cyl_z)), world, translate(-2.1,2.1,2.5)*rotate(30, -20, 0), schott("N-LAK9"))
# Union(Union(cyl_x, cyl_y), cyl_z, world)
Intersect(Intersect(cyl_x, cyl_y), cyl_z, world)
# Intersect(cyl_x, cyl_y, world)
# Union(cyl_y, cyl_z, world)
# Union(cyl_z, cyl_x, world)

camera = PinholeCamera((256, 256), parent=world, transform=translate(0, 0, -4) * rotate(0, 0, 0))

from raysect.vtk import visualise_scenegraph

visualise_scenegraph(camera)
