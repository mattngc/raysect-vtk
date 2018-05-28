
import vtk


cone_source = vtk.vtkConeSource()
cone_source.SetHeight(3)
cone_source.SetRadius(1)
cone_source.SetResolution(10)

cone_mapper = vtk.vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())

cone_actor = vtk.vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_properties = cone_actor.GetProperty()
cone_properties.SetColor(1.0, 0.3882, 0.2784)
cone_properties.SetDiffuse(0.7)
cone_properties.SetSpecular(0.4)
cone_properties.SetSpecularPower(20)


# linear transform matrix
t1 = vtk.vtkMatrixToLinearTransform()
m1 = vtk.vtkMatrix4x4()
t1.SetInput(m1)
m1.SetElement(0, 0, 1)
m1.SetElement(0, 1, 0)
m1.SetElement(0, 2, 0)
m1.SetElement(0, 3, 0)
m1.SetElement(1, 0, 0)
m1.SetElement(1, 1, 1)
m1.SetElement(1, 2, 0)
m1.SetElement(1, 3, 2)
m1.SetElement(2, 0, 0)
m1.SetElement(2, 1, 0)
m1.SetElement(2, 2, 1)
m1.SetElement(2, 3, 0)
m1.SetElement(3, 0, 0)
m1.SetElement(3, 1, 0)
m1.SetElement(3, 2, 0)
m1.SetElement(3, 3, 1)
transform_filter = vtk.vtkTransformPolyDataFilter()
transform_filter.SetInputConnection(cone_source.GetOutputPort())
transform_filter.SetTransform(t1)




cone_mapper2 = vtk.vtkPolyDataMapper()
cone_mapper2.SetInputConnection(transform_filter.GetOutputPort())
transformed_actor = vtk.vtkActor()
transformed_actor.SetMapper(cone_mapper2)
cone_properties2 = transformed_actor.GetProperty()
cone_properties2.SetColor(0.2, 0.63, 0.79)
cone_properties2.SetDiffuse(0.7)
cone_properties2.SetSpecular(0.4)
cone_properties2.SetSpecularPower(20)

# // Set up the transform filter
# vtkSmartPointer<vtkTransform> translation =    vtkSmartPointer<vtkTransform>::New();
# translation->Translate(1.0, 2.0, 3.0);
# vtkSmartPointer<vtkTransformPolyDataFilter> transformFilter =    vtkSmartPointer<vtkTransformPolyDataFilter>::New();
# transformFilter->SetInputConnection(sphereSource->GetOutputPort());
# transformFilter->SetTransform(translation);  transformFilter->Update();
# // Set up the actor to display the transformed polydata
#
# vtkSmartPointer<vtkPolyDataMapper> transformedMapper =
#   vtkSmartPointer<vtkPolyDataMapper>::New();
# transformedMapper->SetInputConnection(transformFilter->GetOutputPort());
# vtkSmartPointer<vtkActor> transformedActor =
#   vtkSmartPointer<vtkActor>::New();
# transformedActor->SetMapper(transformedMapper);  transformedActor->GetProperty()->SetColor(0,1,0);

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren.AddActor(cone_actor)
ren.AddActor(transformed_actor)
ren.SetBackground(0, 0, 0)
renWin.SetSize(200, 200)

iren.Initialize()
ren.ResetCamera()
renWin.Render()
iren.Start()
