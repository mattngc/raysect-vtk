
import vtk
from raysect.core import translate, rotate, rotate_x, rotate_z
from raysect.primitive import Cylinder
from raysect.vtk.utility import convert_to_vtk_transform


# cyl_x = Cylinder(1, 4.2, transform=rotate(90, 0, 0)*translate(0, 0, -2.1))
# cyl_y = Cylinder(1, 4.2, transform=rotate(0, 90, 0)*translate(0, 0, -2.1))
# cyl_z = Cylinder(1, 4.2, transform=rotate(0, 0, 0)*translate(0, 0, -2.1))

cylinder_source1 = vtk.vtkCylinderSource()
cylinder_source1.SetRadius(1)
cylinder_source1.SetHeight(4.2)
cylinder_source1.SetResolution(50)
cylinder_source1.Update()
transform_filter = vtk.vtkTransformPolyDataFilter()
transform_filter.SetInputConnection(cylinder_source1.GetOutputPort())
transform_filter.SetTransform(convert_to_vtk_transform(rotate_x(90)))
transform_filter.Update()
tris1 = vtk.vtkTriangleFilter()
tris1.SetInputData(transform_filter.GetOutput())


cylinder_source2 = vtk.vtkCylinderSource()
cylinder_source2.SetRadius(1)
cylinder_source2.SetHeight(4.2)
cylinder_source2.SetResolution(50)
cylinder_source2.Update()
transform_filter = vtk.vtkTransformPolyDataFilter()
transform_filter.SetInputConnection(cylinder_source2.GetOutputPort())
transform_filter.SetTransform(convert_to_vtk_transform(rotate_z(90)))
transform_filter.Update()
tris2 = vtk.vtkTriangleFilter()
tris2.SetInputData(transform_filter.GetOutput())


booleanOperation1 = vtk.vtkBooleanOperationPolyDataFilter()
booleanOperation1.SetOperationToUnion()
booleanOperation1.SetInputConnection(0, tris1.GetOutputPort())
booleanOperation1.SetInputConnection(1, tris2.GetOutputPort())
booleanOperation1.Update()
bool_tris = vtk.vtkTriangleFilter()
bool_tris.SetInputData(booleanOperation1.GetOutput())


cylinder_source3 = vtk.vtkCylinderSource()
cylinder_source3.SetRadius(1)
cylinder_source3.SetHeight(4.2)
cylinder_source3.SetResolution(50)
cylinder_source3.Update()
tris3 = vtk.vtkTriangleFilter()
tris3.SetInputData(cylinder_source3.GetOutput())

booleanOperation2 = vtk.vtkBooleanOperationPolyDataFilter()
booleanOperation2.SetOperationToUnion()
booleanOperation2.SetInputConnection(0, bool_tris.GetOutputPort())
booleanOperation2.SetInputConnection(1, tris3.GetOutputPort())
booleanOperation2.Update()

booleanOperationMapper = vtk.vtkPolyDataMapper()
booleanOperationMapper.SetInputConnection(booleanOperation2.GetOutputPort())
booleanOperationMapper.ScalarVisibilityOff()

booleanOperationActor = vtk.vtkActor()
booleanOperationActor.SetMapper(booleanOperationMapper)

renderer = vtk.vtkRenderer()
renderer.AddViewProp(booleanOperationActor)
renderer.SetBackground(.1, .2, .3)
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renWinInteractor = vtk.vtkRenderWindowInteractor()
renWinInteractor.SetRenderWindow(renderWindow)


renderWindow.Render()
renWinInteractor.Start()
