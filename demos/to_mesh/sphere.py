
from raysect.optical import World, translate, rotate
from raysect.optical.observer import PinholeCamera
from raysect.primitive import Sphere

from raysect_vtk.primitives.to_mesh import sphere_to_mesh


world = World()
sphere = Sphere()
sphere_mesh = sphere_to_mesh(sphere, subdivision_count=1)
sphere_mesh.parent = world


camera = PinholeCamera((256, 256), fov=40, parent=world, transform=translate(0, 0.16, -0.4) * rotate(0, -12, 0))


from raysect_vtk import visualise_scenegraph

visualise_scenegraph(camera, focal_distance=3, zoom=0.5)
