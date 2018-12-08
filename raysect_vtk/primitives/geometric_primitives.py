
import vtk

from raysect.primitive import Box, Sphere, Cylinder, Cone, Mesh

from raysect_vtk.utility import convert_to_vtk_transform
from raysect_vtk.primitives.to_mesh import box_to_mesh, sphere_to_mesh, cylinder_to_mesh, cone_to_mesh


class VTKGeometricPrimitive:

    def __init__(self, raysect_primitive, vtk_polydata):

        self._raysect_primitive = raysect_primitive

        transform = convert_to_vtk_transform(raysect_primitive.transform)
        self._transform = transform

        self._geometry_source = vtk_polydata

        transform_filter = vtk.vtkTransformPolyDataFilter()
        if isinstance(vtk_polydata, vtk.vtkPolyData):
            transform_filter.SetInputData(vtk_polydata)
        elif isinstance(vtk_polydata, vtk.vtkPolyDataAlgorithm):
            transform_filter.SetInputConnection(vtk_polydata.GetOutputPort())
        else:
            raise TypeError("Incompatible vtk object given to VTKGeometricPrimitive.")
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
            raise TypeError("'raysect_box' must be a Raysect Box primitive,"
                            "wrong type '{}' given.".format(type(raysect_box)))

        raysect_mesh = box_to_mesh(raysect_box)
        vtk_mesh = create_vtk_mesh_representation(raysect_mesh.data.vertices, raysect_mesh.data.triangles)

        super().__init__(raysect_box, vtk_mesh)


class VTKSphere(VTKGeometricPrimitive):

    def __init__(self, raysect_sphere):

        if not isinstance(raysect_sphere, Sphere):
            raise TypeError("'raysect_sphere' must be a Raysect Sphere primitive,"
                            "wrong type '{}' given.".format(type(raysect_sphere)))

        raysect_mesh = sphere_to_mesh(raysect_sphere)
        vtk_mesh = create_vtk_mesh_representation(raysect_mesh.data.vertices, raysect_mesh.data.triangles)

        super().__init__(raysect_sphere, vtk_mesh)


class VTKCylinder(VTKGeometricPrimitive):

    def __init__(self, raysect_cylinder):

        if not isinstance(raysect_cylinder, Cylinder):
            raise TypeError("'raysect_cylinder' must be a Raysect Cylinder primitive,"
                            "wrong type '{}' given.".format(type(raysect_cylinder)))

        raysect_mesh = cylinder_to_mesh(raysect_cylinder)
        vtk_mesh = create_vtk_mesh_representation(raysect_mesh.data.vertices, raysect_mesh.data.triangles)

        super().__init__(raysect_cylinder, vtk_mesh)


class VTKCone(VTKGeometricPrimitive):

    def __init__(self, raysect_cone):

        if not isinstance(raysect_cone, Cone):
            raise TypeError("'raysect_cone' must be a Raysect Cone primitive,"
                            "wrong type '{}' given.".format(type(raysect_cone)))

        raysect_mesh = cone_to_mesh(raysect_cone)
        vtk_mesh = create_vtk_mesh_representation(raysect_mesh.data.vertices, raysect_mesh.data.triangles)

        super().__init__(raysect_cone, vtk_mesh)


class VTKMesh(VTKGeometricPrimitive):

    def __init__(self, raysect_mesh):

        if not isinstance(raysect_mesh, Mesh):
            raise TypeError("Must be a Raysect Mesh.")

        vtk_mesh = create_vtk_mesh_representation(raysect_mesh.data.vertices, raysect_mesh.data.triangles)

        super().__init__(raysect_mesh, vtk_mesh)


def create_vtk_mesh_representation(vertices, triangles):

    # We'll create the building blocks of polydata including data attributes.
    vtk_mesh = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    polys = vtk.vtkCellArray()

    # Load the point, cell, and data attributes.
    for i, xi in enumerate(vertices):
        points.InsertPoint(i, xi)
    for pt in triangles:
        # make an ID list for each cell
        vil = vtk.vtkIdList()
        for j in pt:
            vil.InsertNextId(int(j))
        # Define the cell through the list of point IDs.
        polys.InsertNextCell(vil)

    # We now assign the pieces to the vtkPolyData.
    vtk_mesh.SetPoints(points)
    vtk_mesh.SetPolys(polys)

    return vtk_mesh
