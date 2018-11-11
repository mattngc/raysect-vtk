
import vtk

from raysect.core import Node
from raysect.primitive import Box, Sphere, Cylinder, Cone, Parabola, Mesh, Intersect, Union, Subtract

from raysect_vtk.utility import convert_to_vtk_transform
from raysect_vtk.primitives.geometric_primitives import VTKBox, VTKSphere, VTKCylinder, VTKCone, VTKMesh, VTKGeometricPrimitive


def map_raysect_element_to_vtk(raysect_element):

    if isinstance(raysect_element, Box):
        print("loading box", raysect_element)
        return VTKBox(raysect_element)

    elif isinstance(raysect_element, Sphere):
        print("loading sphere", raysect_element)
        return VTKSphere(raysect_element)

    elif isinstance(raysect_element, Cylinder):
        print("loading cylinder", raysect_element)
        return VTKCylinder(raysect_element)

    elif isinstance(raysect_element, Cone):
        print("loading cone", raysect_element)
        return VTKCone(raysect_element)

    elif isinstance(raysect_element, Parabola):
        print("loading parabola", raysect_element)
        raise NotImplementedError("Parabolic primitives are not supported for visualisation at this time.")

    elif isinstance(raysect_element, Mesh):
        print("loading mesh", raysect_element)
        return VTKMesh(raysect_element)

    elif isinstance(raysect_element, Intersect):
        return VTKIntersection(raysect_element)

    elif isinstance(raysect_element, Union):
        return VTKUnion(raysect_element)

    elif isinstance(raysect_element, Subtract):
        return VTKSubtract(raysect_element)

    elif isinstance(raysect_element, Node):
        print("loading node", raysect_element)
        return VTKAssembly(raysect_element)


class VTKAssembly:

    def __init__(self, raysect_node):

        if not isinstance(raysect_node, Node):
            raise TypeError("A VTKNode can only be constructed from a Raysect Node object.")

        assembly = vtk.vtkAssembly()
        assembly.SetUserTransform(convert_to_vtk_transform(raysect_node.transform))
        for child in raysect_node.children:
            vtk_part = map_raysect_element_to_vtk(child)
            assembly.AddPart(vtk_part.actor)

        self.assembly = assembly


class VTKCSGOperation:

    def __init__(self, raysect_csg_primitive):

        # need to get the geometry source for each primitive
        self.raysect_primitive = raysect_csg_primitive

        primitive_a = map_raysect_element_to_vtk(raysect_csg_primitive.primitive_a)
        source_a_tris = vtk.vtkTriangleFilter()
        source_a_tris.SetInputData(primitive_a.transform_filter.GetOutput())
        self.source_a_tri_filter = source_a_tris

        primitive_b = map_raysect_element_to_vtk(raysect_csg_primitive.primitive_b)
        source_b_tris = vtk.vtkTriangleFilter()
        source_b_tris.SetInputData(primitive_b.transform_filter.GetOutput())
        self.source_b_tri_filter = source_b_tris

        boolean_operation = vtk.vtkBooleanOperationPolyDataFilter()
        self.boolean_operation = boolean_operation
        self._set_boolean_operation()
        boolean_operation.SetInputConnection(0, source_a_tris.GetOutputPort())
        boolean_operation.SetInputConnection(1, source_b_tris.GetOutputPort())
        boolean_operation.Update()

        transform_filter = vtk.vtkTransformPolyDataFilter()
        transform_filter.SetInputConnection(boolean_operation.GetOutputPort())
        transform_filter.SetTransform(convert_to_vtk_transform(raysect_csg_primitive.transform))
        transform_filter.Update()
        self.transform_filter = transform_filter

        booleanOperationMapper = vtk.vtkPolyDataMapper()
        booleanOperationMapper.SetInputConnection(transform_filter.GetOutputPort())
        booleanOperationMapper.ScalarVisibilityOff()
        self.mapper = booleanOperationMapper

        booleanOperationActor = vtk.vtkActor()
        booleanOperationActor.SetMapper(booleanOperationMapper)
        self.actor = booleanOperationActor

    def _set_boolean_operation(self):
        raise NotImplementedError("This method must be implemented by the inheriting class.")


class VTKIntersection(VTKCSGOperation):

    def __init__(self, raysect_intersect):

        if not isinstance(raysect_intersect, Intersect):
            raise TypeError("A Raysect CSG Intersection object must be supplied.")

        super().__init__(raysect_intersect)

    def _set_boolean_operation(self):
        self.boolean_operation.SetOperationToIntersection()


class VTKUnion(VTKCSGOperation):

    def __init__(self, raysect_union):

        if not isinstance(raysect_union, Union):
            raise TypeError("A Raysect CSG Union object must be supplied.")

        super().__init__(raysect_union)

    def _set_boolean_operation(self):
        self.boolean_operation.SetOperationToUnion()


class VTKSubtract(VTKCSGOperation):

    def __init__(self, raysect_subtract):

        if not isinstance(raysect_subtract, Subtract):
            raise TypeError("A Raysect CSG Subtract object must be supplied.")

        super().__init__(raysect_subtract)

    def _set_boolean_operation(self):
        self.boolean_operation.SetOperationToDifference()
