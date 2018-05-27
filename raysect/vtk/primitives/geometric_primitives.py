
import vtk

from raysect.core import Point3D
from raysect.primitive import Box, Sphere, Cylinder, Cone

from raysect.vtk.utility import convert_to_vtk_transform


def convert_box_to_vtk(raysect_box):

    if not isinstance(raysect_box, Box):
        raise TypeError("Must be a Raysect Box.")

    lower = raysect_box.lower
    upper = raysect_box.upper

    x_width = upper.x - lower.x
    y_width = upper.y - lower.y
    z_width = upper.z - lower.z

    box_centre = Point3D((upper.x + lower.x)/2, (upper.y + lower.y)/2, (upper.z + lower.z)/2)

    cube_source = vtk.vtkCubeSource()
    cube_source.SetXLength(x_width)
    cube_source.SetYLength(y_width)
    cube_source.SetZLength(z_width)
    cube_source.SetCenter(box_centre.x, box_centre.y, box_centre.z)

    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetInputConnection(cube_source.GetOutputPort())
    transform_filter.SetTransform(convert_to_vtk_transform(raysect_box.transform))

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transform_filter.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


def convert_sphere_to_vtk(raysect_sphere):

    if not isinstance(raysect_sphere, Sphere):
        raise TypeError("Must be a Raysect Sphere.")

    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetRadius(raysect_sphere.radius)
    sphere_source.SetPhiResolution(50)
    sphere_source.SetThetaResolution(50)

    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetInputConnection(sphere_source.GetOutputPort())
    transform_filter.SetTransform(convert_to_vtk_transform(raysect_sphere.transform))

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transform_filter.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


def convert_cylinder_to_vtk(raysect_cylinder):

    if not isinstance(raysect_cylinder, Cylinder):
        raise TypeError("Must be a Raysect Cylinder.")

    cylinder_source = vtk.vtkCylinderSource()
    cylinder_source.SetRadius(raysect_cylinder.radius)
    cylinder_source.SetHeight(raysect_cylinder.height)
    cylinder_source.SetCenter(0, 0, raysect_cylinder.height/2)
    cylinder_source.SetDirection(0, 0, 1)
    cylinder_source.SetResolution(50)

    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetInputConnection(cylinder_source.GetOutputPort())
    transform_filter.SetTransform(convert_to_vtk_transform(raysect_cylinder.transform))

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transform_filter.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


def convert_cone_to_vtk(raysect_cone):

    if isinstance(raysect_cone, Cone):
        raise TypeError("Must be a Raysect Cone.")

    cone_source = vtk.vtkConeSource()
    cone_source.SetHeight(raysect_cone.height)
    cone_source.SetRadius(raysect_cone.radius)
    cone_source.SetCenter(0, 0, raysect_cone.height/2)
    cone_source.SetDirection(0, 0, 1)
    cone_source.SetResolution(50)

    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetInputConnection(cone_source.GetOutputPort())
    transform_filter.SetTransform(convert_to_vtk_transform(raysect_cone.transform))

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transform_filter.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor
