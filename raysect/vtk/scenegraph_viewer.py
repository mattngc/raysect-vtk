
import vtk

from raysect.core import World, Node
from raysect.vtk.primitives.mapper import map_raysect_element_to_vtk


def visualise_scenegraph(world):

    if not isinstance(world, World):
        raise TypeError("The vtk visualisation function takes a scene-graph World object as its argument.")

    # Add the actors to the renderer
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0, 0, 0)
    for child in world.children:
        renderer.AddActor(map_raysect_element_to_vtk(child))

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    renWin.SetSize(512, 512)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()

    # Start the event loop.
    iren.Start()
