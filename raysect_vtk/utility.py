
import vtk


def convert_to_vtk_transform(transform):
    """
    Converts a Raysect AffineMatrix3D to an equivalent VTK vtkMatrixToLinearTransform.

    :param AffineMatrix3D transform: The Raysect transform matrix to be converted to VTK format.
    :rtype: vtk.vtkMatrixToLinearTransform
    """

    # linear transform matrix
    t1 = vtk.vtkMatrixToLinearTransform()
    m1 = vtk.vtkMatrix4x4()
    t1.SetInput(m1)
    m1.SetElement(0, 0, transform[0, 0])
    m1.SetElement(0, 1, transform[0, 1])
    m1.SetElement(0, 2, transform[0, 2])
    m1.SetElement(0, 3, transform[0, 3])
    m1.SetElement(1, 0, transform[1, 0])
    m1.SetElement(1, 1, transform[1, 1])
    m1.SetElement(1, 2, transform[1, 2])
    m1.SetElement(1, 3, transform[1, 3])
    m1.SetElement(2, 0, transform[2, 0])
    m1.SetElement(2, 1, transform[2, 1])
    m1.SetElement(2, 2, transform[2, 2])
    m1.SetElement(2, 3, transform[2, 3])
    m1.SetElement(3, 0, transform[3, 0])
    m1.SetElement(3, 1, transform[3, 1])
    m1.SetElement(3, 2, transform[3, 2])
    m1.SetElement(3, 3, transform[3, 3])

    return t1
