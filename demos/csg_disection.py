
from matplotlib.pyplot import *
from numpy import array

from raysect.primitive import Sphere, Box, Cylinder, Union, Intersect, Subtract
from raysect.optical import World, translate, rotate, Point3D, d65_white, InterpolatedSF
from raysect.optical.material.emitter import UniformSurfaceEmitter, Checkerboard
from raysect.optical.material.dielectric import Dielectric, Sellmeier
from raysect.optical.library import schott
from raysect.optical.observer import PinholeCamera, RGBPipeline2D, SpectralPowerPipeline2D

world = World()

s1 = Sphere(1.0, transform=translate(0, 0, 0.25))
s2 = Sphere(1.0, transform=translate(0, 0, -0.25))
intersection = Intersect(s1, s2, transform=translate(0, 0, 0))
s3 = Sphere(1.0, transform=translate(0, 0.5, 0))
intersection = Union(intersection, s3, world, transform=translate(0.5, 0, 0))


# cyl_x = Cylinder(1, 4.2, transform=rotate(90, 0, 0)*translate(0, 0, -2.1))
# cyl_y = Cylinder(1, 4.2, transform=rotate(0, 90, 0)*translate(0, 0, -2.1))
# cyl_z = Cylinder(1, 4.2, transform=rotate(0, 0, 0)*translate(0, 0, -2.1))
# cube = Box(Point3D(-1.5, -1.5, -1.5), Point3D(1.5, 1.5, 1.5))
# sphere = Sphere(2.0)
#
# # Intersect(sphere, Subtract(cube, Union(Union(cyl_x, cyl_y), cyl_z)), world, translate(-2.1,2.1,2.5)*rotate(30, -20, 0), schott("N-LAK9"))
# Union(Union(cyl_x, cyl_y), cyl_z, world)


camera = PinholeCamera((256, 256), parent=world, transform=translate(0, 0, -4) * rotate(0, 0, 0))

# from raysect.vtk.scenegraph_viewer import map_raysect_element_to_vtk
# s1_actor = map_raysect_element_to_vtk(s1)


from raysect.vtk import visualise_scenegraph

visualise_scenegraph(camera)
