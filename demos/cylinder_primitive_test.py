
from matplotlib.pyplot import *
from numpy import array

from raysect.primitive import Sphere, Box, Cylinder, Union, Intersect, Subtract
from raysect.optical import World, translate, rotate, Point3D, d65_white, InterpolatedSF
from raysect.optical.material.emitter import UniformSurfaceEmitter, Checkerboard
from raysect.optical.material.dielectric import Dielectric, Sellmeier
from raysect.optical.library import schott
from raysect.optical.observer import PinholeCamera, RGBPipeline2D, SpectralPowerPipeline2D

world = World()

c1 = Cylinder(1.0, height=3, transform=translate(0, 0, 0), parent=world)

camera = PinholeCamera((256, 256), parent=world, transform=translate(0, 0, -4) * rotate(0, 0, 0))

from raysect.vtk import visualise_scenegraph

visualise_scenegraph(camera)
