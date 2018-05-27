
import vtk

from raysect.core import Node
from raysect.primitive import Box, Sphere, Cylinder, Cone, Parabola

from raysect.vtk.utility import convert_to_vtk_transform
from raysect.vtk.primitives.geometric_primitives import convert_box_to_vtk, convert_sphere_to_vtk,\
    convert_cylinder_to_vtk, convert_cone_to_vtk


def map_raysect_element_to_vtk(raysect_element):

    if isinstance(raysect_element, Box):
        return convert_box_to_vtk(raysect_element)

    elif isinstance(raysect_element, Sphere):
        return convert_sphere_to_vtk(raysect_element)

    elif isinstance(raysect_element, Cylinder):
        return convert_cylinder_to_vtk(raysect_element)

    elif isinstance(raysect_element, Cone):
        return convert_cone_to_vtk(raysect_element)

    elif isinstance(raysect_element, Parabola):
        raise TypeError("Parabolic primitives are not supported for visualisation at this time.")

    elif isinstance(raysect_element, Node):
        return convert_node_to_vtk(raysect_element)


def convert_node_to_vtk(raysect_node):

    if not isinstance(raysect_node, Node):
        raise TypeError("A VTKNode can only be constructed from a Raysect Node object.")

    assembly = vtk.vtkAssembly()
    # assembly.SetUserTransform(convert_to_vtk_transform(raysect_node.transform))
    for child in raysect_node.children:
        vtk_part = map_raysect_element_to_vtk(child)
        assembly.AddPart(vtk_part)

    return assembly
