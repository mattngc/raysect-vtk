
import vtk

from raysect.core import Point3D, rotate_x
from raysect.primitive import Box, Sphere, Cylinder, Cone

from raysect_vtk.utility import convert_to_vtk_transform


class VTKGeometricPrimitive:

    def __init__(self, raysect_primitive, geometry_source):

        self._raysect_primitive = raysect_primitive

        transform = convert_to_vtk_transform(raysect_primitive.transform)
        self._transform = transform

        self._geometry_source = geometry_source

        transform_filter = vtk.vtkTransformPolyDataFilter()
        transform_filter.SetInputConnection(geometry_source.GetOutputPort())
        transform_filter.SetTransform(self.transform)
        transform_filter.Update()
        self._transform_filter = transform_filter

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(transform_filter.GetOutputPort())
        self._mapper = mapper

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self._actor = actor

    @property
    def raysect_primitive(self):
        return self._raysect_primitive

    @property
    def transform(self):
        return self._transform

    @property
    def geometry_source(self):
        return self._geometry_source

    @property
    def transform_filter(self):
        return self._transform_filter

    @property
    def mapper(self):
        return self._mapper

    @property
    def actor(self):
        return self._actor


class VTKBox(VTKGeometricPrimitive):

    def __init__(self, raysect_box):

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
        cube_source.Update()

        super().__init__(raysect_box, cube_source)


class VTKSphere(VTKGeometricPrimitive):

    def __init__(self, raysect_sphere):

        if not isinstance(raysect_sphere, Sphere):
            raise TypeError("Must be a Raysect Sphere.")

        sphere_source = vtk.vtkSphereSource()
        sphere_source.SetRadius(raysect_sphere.radius)
        sphere_source.SetPhiResolution(50)
        sphere_source.SetThetaResolution(50)
        sphere_source.Update()

        super().__init__(raysect_sphere, sphere_source)


class VTKCylinder(VTKGeometricPrimitive):

    def __init__(self, raysect_cylinder):

        if not isinstance(raysect_cylinder, Cylinder):
            raise TypeError("Must be a Raysect Cylinder.")

        cylinder_source = vtk.vtkCylinderSource()
        cylinder_source.SetRadius(raysect_cylinder.radius)
        cylinder_source.SetHeight(raysect_cylinder.height)
        cylinder_source.SetCenter(0, raysect_cylinder.height/2, 0)
        cylinder_source.SetResolution(50)
        cylinder_source.Update()

        self._raysect_primitive = raysect_cylinder

        # Note - VTK cylinders are aligned along the y axis
        transform = convert_to_vtk_transform(raysect_cylinder.transform * rotate_x(90))
        self._transform = transform

        self._geometry_source = cylinder_source

        transform_filter = vtk.vtkTransformPolyDataFilter()
        transform_filter.SetInputConnection(cylinder_source.GetOutputPort())
        transform_filter.SetTransform(self.transform)
        transform_filter.Update()
        self._transform_filter = transform_filter

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(transform_filter.GetOutputPort())
        self._mapper = mapper

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self._actor = actor


class VTKCone(VTKGeometricPrimitive):

    def __init__(self, raysect_cone):

        if isinstance(raysect_cone, Cone):
            raise TypeError("Must be a Raysect Cone.")

        cone_source = vtk.vtkConeSource()
        cone_source.SetHeight(raysect_cone.height)
        cone_source.SetRadius(raysect_cone.radius)
        cone_source.SetCenter(0, 0, raysect_cone.height/2)
        cone_source.SetDirection(0, 0, 1)
        cone_source.SetResolution(50)
        cone_source.Update()

        super().__init__(raysect_cone, cone_source)
