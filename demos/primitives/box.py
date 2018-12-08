
from raysect.optical import World, translate, rotate, rotate_basis, Vector3D
from raysect.optical.observer import PinholeCamera
from raysect.primitive import Box


world = World()
box = Box(parent=world, transform=translate(1, 0, 0)*rotate_basis(Vector3D(1, 1, 0), Vector3D(0, 0, 1)))

camera = PinholeCamera((256, 256), fov=40, parent=world, transform=translate(0, 0.16, -0.4) * rotate(0, -12, 0))


from raysect_vtk import visualise_scenegraph

visualise_scenegraph(camera, focal_distance=3, zoom=0.5)
