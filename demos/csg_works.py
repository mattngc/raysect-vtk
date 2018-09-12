
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

camera = PinholeCamera((256, 256), parent=world, transform=translate(0, 0, -4) * rotate(0, 0, 0))

from raysect_vtk import visualise_scenegraph

visualise_scenegraph(camera)
