
from raysect.optical import World, translate, rotate
from raysect.optical.observer import PinholeCamera
from raysect.primitive import Sphere


world = World()
sphere = Sphere(parent=world, transform=translate(2, 0, 0))


camera = PinholeCamera((256, 256), fov=40, parent=world, transform=translate(0, 0.16, -0.4) * rotate(0, -12, 0))


from raysect_vtk import visualise_scenegraph

visualise_scenegraph(camera, focal_distance=3, zoom=0.5)
