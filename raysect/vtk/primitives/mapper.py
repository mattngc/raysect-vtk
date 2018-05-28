
import vtk

from raysect.core import Node
from raysect.primitive import Box, Sphere, Cylinder, Cone, Parabola, Intersect

from raysect.vtk.utility import convert_to_vtk_transform
from raysect.vtk.primitives.geometric_primitives import VTKBox, VTKSphere, VTKCylinder, VTKCone


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

    elif isinstance(raysect_element, Intersect):
        return convert_csg_intersect_to_vtk(raysect_element)

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


def convert_csg_intersect_to_vtk(raysect_intersect):

    if not isinstance(raysect_intersect, Intersect):
        raise TypeError("A Raysect CSG intersection object must be supplied.")

    # need to get the geometry source for each primitive
    primitive_a = map_raysect_element_to_vtk(raysect_intersect.primitive_a)
    mapper_a = primitive_a.GetMapper()
    polydata_filter_a = mapper_a.GetInputConnection(0, 0).GetProducer()
    source_a = polydata_filter_a.GetInputConnection(0, 0).GetProducer()
    source_a.Update()

    source_a_tris = vtk.vtkTriangleFilter()
    source_a_tris.SetInputData(source_a.GetOutput())

    primitive_b = map_raysect_element_to_vtk(raysect_intersect.primitive_b)
    mapper_b = primitive_b.GetMapper()
    polydata_filter_b = mapper_b.GetInputConnection(0, 0).GetProducer()
    source_b = polydata_filter_b.GetInputConnection(0, 0).GetProducer()
    source_b.Update()

    source_b_tris = vtk.vtkTriangleFilter()
    source_b_tris.SetInputData(source_b.GetOutput())

    print("Starting boolean operations")

    booleanOperation = vtk.vtkBooleanOperationPolyDataFilter()
    # booleanOperation.SetOperationToUnion()
    booleanOperation.SetOperationToIntersection()
    # booleanOperation.SetOperationToDifference()

    booleanOperation.SetInputConnection(0, source_a_tris.GetOutputPort())
    booleanOperation.SetInputConnection(1, source_b_tris.GetOutputPort())
    booleanOperation.Update()

    booleanOperationMapper = vtk.vtkPolyDataMapper()
    booleanOperationMapper.SetInputConnection(booleanOperation.GetOutputPort())
    booleanOperationMapper.ScalarVisibilityOff()

    booleanOperationActor = vtk.vtkActor()
    booleanOperationActor.SetMapper(booleanOperationMapper)

    print("Ending boolean operations")

    return booleanOperationActor

# In [6]: mapper.GetInputConnection(0, 0)
# Out[6]: (vtkCommonExecutionModelPython.vtkAlgorithmOutput)0x7f5b4ee33e28
#
# In [7]: mapper.GetInputConnection(0, 0).GetProducer()
# Out[7]: (vtkFiltersGeneralPython.vtkTransformPolyDataFilter)0x7f5af84ffbe8
#
# In [8]: polydata_filter = mapper.GetInputConnection(0, 0).GetProducer()
#
# In [9]: polydata_filter.GetInputConnection(0,0)
# Out[9]: (vtkCommonExecutionModelPython.vtkAlgorithmOutput)0x7f5af3a0c8e8
#
# In [10]: polydata_filter.GetInputConnection(0,0).GetProducer()
# Out[10]: (vtkFiltersSourcesPython.vtkSphereSource)0x7f5b4ee33dc8
#
# In [11]: sphere_source = polydata_filter.GetInputConnection(0,0).GetProducer()
#
# In [12]: sphere_source
# Out[12]: (vtkFiltersSourcesPython.vtkSphereSource)0x7f5b4ee33dc8

