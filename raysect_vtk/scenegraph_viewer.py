
import vtk

from raysect.core import Observer, World, Point3D, Vector3D
from raysect_vtk.primitives.mapper import map_raysect_element_to_vtk, VTKAssembly


def visualise_scenegraph(camera, focal_distance=1, zoom=1):

    if not isinstance(camera, Observer):
        raise TypeError("The vtk visualisation function takes a Raysect Observer object as its argument.")

    world = camera.root

    if not isinstance(world, World):
        raise TypeError("The vtk visualisation function requires the Raysect Observer object to be connected to a valid scene-graph.")

    # Add the actors to the renderer
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0, 0, 0)
    for child in world.children:
        vtk_element = map_raysect_element_to_vtk(child)
        if isinstance(vtk_element, VTKAssembly):
            renderer.AddActor(vtk_element.assembly)
        else:
            renderer.AddActor(vtk_element.actor)

    axes = vtk.vtkAxesActor()
    renderer.AddActor(axes)

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    renWin.SetSize(512, 512)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    iren.Initialize()

    camera_origin = Point3D(0, 0, 0).transform(camera.transform)
    camera_direction = Vector3D(0, 0, 1).transform(camera.transform)
    up_direction = Vector3D(0, 1, 0).transform(camera.transform)
    focal_point = camera_origin + camera_direction * focal_distance

    vtk_camera = vtk.vtkCamera()
    vtk_camera.SetPosition(camera_origin.x, camera_origin.y, camera_origin.z)
    vtk_camera.SetFocalPoint(focal_point.x, focal_point.y, focal_point.z)
    vtk_camera.SetViewUp(up_direction.x, up_direction.y, up_direction.z)
    vtk_camera.ComputeViewPlaneNormal()
    vtk_camera.SetDistance(focal_distance)
    vtk_camera.Zoom(zoom)
    renderer.SetActiveCamera(vtk_camera)
    renderer.SetBackground(1.0, 0.9688, 0.8594)

    # Start the event loop.
    iren.Start()
