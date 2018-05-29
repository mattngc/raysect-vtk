
import vtk
from raysect.core import translate
from raysect.vtk.utility import convert_to_vtk_transform


sphereSource1 = vtk.vtkSphereSource()
# sphereSource1.SetCenter(0.25, 0, 0)
sphereSource1.SetPhiResolution(50)
sphereSource1.SetThetaResolution(50)
sphereSource1.Update()
transform_filter1 = vtk.vtkTransformPolyDataFilter()
transform_filter1.SetInputConnection(sphereSource1.GetOutputPort())
transform_filter1.SetTransform(convert_to_vtk_transform(translate(0.25, 0, 0)))
transform_filter1.Update()
sphere1Tri = vtk.vtkTriangleFilter()
sphere1Tri.SetInputData(transform_filter1.GetOutput())

sphereSource2 = vtk.vtkSphereSource()
# sphereSource2.SetCenter(-0.25, 0, 0)
sphereSource2.SetPhiResolution(50)
sphereSource2.SetThetaResolution(50)
sphereSource2.Update()
transform_filter2 = vtk.vtkTransformPolyDataFilter()
transform_filter2.SetInputConnection(sphereSource2.GetOutputPort())
transform_filter2.SetTransform(convert_to_vtk_transform(translate(-0.25, 0, 0)))
transform_filter2.Update()
sphere2Tri = vtk.vtkTriangleFilter()
sphere2Tri.SetInputData(transform_filter2.GetOutput())


booleanOperation = vtk.vtkBooleanOperationPolyDataFilter()
# booleanOperation.SetOperationToUnion()
booleanOperation.SetOperationToIntersection()
# booleanOperation.SetOperationToDifference()

booleanOperation.SetInputConnection(0, sphere1Tri.GetOutputPort())
booleanOperation.SetInputConnection(1, sphere2Tri.GetOutputPort())
booleanOperation.Update()

transform_filter3 = vtk.vtkTransformPolyDataFilter()
transform_filter3.SetInputConnection(booleanOperation.GetOutputPort())
transform_filter3.SetTransform(convert_to_vtk_transform(translate(0, 0.5, 0)))
transform_filter3.Update()

booleanOperationMapper = vtk.vtkPolyDataMapper()
booleanOperationMapper.SetInputConnection(transform_filter3.GetOutputPort())
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