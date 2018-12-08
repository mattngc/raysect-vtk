
from raysect.optical import World, translate, rotate
from raysect.optical.observer import PinholeCamera
from raysect.primitive import import_obj


world = World()
mesh = import_obj("/home/matt/pyFusion/raysect/demos/resources/stanford_bunny.obj", parent=world,
                  transform=translate(0, 0, 0)*rotate(165, 0, 0))


camera = PinholeCamera((256, 256), fov=40, parent=world, transform=translate(0, 0.16, -0.4) * rotate(0, -12, 0))


from raysect_vtk import visualise_scenegraph

visualise_scenegraph(camera, focal_distance=3, zoom=0.5)


