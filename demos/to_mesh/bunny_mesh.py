
import vtk

from raysect.optical import World, translate, rotate
from raysect.primitive import import_obj


def mkVtkIdList(it):
    """
    Makes a vtkIdList from a Python iterable. I'm kinda surprised that
     this is necessary, since I assumed that this kind of thing would
     have been built into the wrapper and happen transparently, but it
     seems not.

    :param it: A python iterable.
    :return: A vtkIdList
    """
    vil = vtk.vtkIdList()
    for i in it:
        vil.InsertNextId(int(i))
    return vil


world = World()
mesh = import_obj("/home/matt/pyFusion/raysect/demos/resources/stanford_bunny.obj", parent=world,
                  transform=translate(0, 0, 0)*rotate(165, 0, 0))


# We'll create the building blocks of polydata including data attributes.
cube = vtk.vtkPolyData()
points = vtk.vtkPoints()
polys = vtk.vtkCellArray()

# Load the point, cell, and data attributes.
for i, xi in enumerate(mesh.data.vertices):
    points.InsertPoint(i, xi)
for pt in mesh.data.triangles:
    polys.InsertNextCell(mkVtkIdList(pt))

# We now assign the pieces to the vtkPolyData.
cube.SetPoints(points)
cube.SetPolys(polys)


# Now we'll look at it.
cubeMapper = vtk.vtkPolyDataMapper()
cubeMapper.SetInputData(cube)

cubeActor = vtk.vtkActor()
cubeActor.SetMapper(cubeMapper)

# The usual rendering stuff.
camera = vtk.vtkCamera()
camera.SetPosition(1, 1, 1)
camera.SetFocalPoint(0, 0, 0)

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

renderer.AddActor(cubeActor)
renderer.SetActiveCamera(camera)
renderer.ResetCamera()

# renderer.SetBackground(vtk.vtkNamedColors().GetColor3d("Cornsilk"))
# renderer.SetBackground(1.0, 0.9688, 0.8594)

renWin.SetSize(600, 600)

# interact with data
renWin.Render()
iren.Start()