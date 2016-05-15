import cv2
from matplotlib import pyplot
from plotly.offline import  init_notebook_mode, iplot
from plotly.graph_objs import *
from scipy import ndimage

init_notebook_mode()

__author__ = 'N'

from vtk.util import numpy_support


import numpy
from gap_reconstruction import gap_reconstruction_func


def vtkImageToNumPy(image, pixelDims):
    pointData = image.GetPointData()
    arrayData = pointData.GetArray(0)
    ArrayDicom = numpy_support.vtk_to_numpy(arrayData)
    ArrayDicom = ArrayDicom.reshape(pixelDims, order='F')

    return ArrayDicom

def plotHeatmap(array, name="plot"):
    data = [
       graph_objs.Heatmap(
            z=array,
            colorscale='Greys'
        )
    ]
    layout = graph_objs.Layout(
        autosize=False,
        title=name
    )
    fig = dict(data=data, layout=layout)

    return iplot(fig)

import vtk
from IPython.display import Image
def vtk_show(renderer, width=400, height=300):
    """
    Takes vtkRenderer instance and returns an IPython Image with the rendering.
    """
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetOffScreenRendering(1)
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(width, height)
    renderWindow.Render()

    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renderWindow)
    windowToImageFilter.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetWriteToMemory(1)
    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    writer.Write()
    data = str(buffer(writer.GetResult()))

    return Image(data)


PathDicom = "./COU/"
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(PathDicom)
reader.Update()

_extent = reader.GetDataExtent()
ConstPixelDims = [_extent[1]-_extent[0]+1, _extent[3]-_extent[2]+1, _extent[5]-_extent[4]+1]
ConstPixelSpacing = reader.GetPixelSpacing()

threshold = vtk.vtkImageThreshold ()
threshold.SetInputConnection(reader.GetOutputPort())
threshold.ThresholdByLower(400)  # remove all soft tissue
threshold.ReplaceInOn()
threshold.SetInValue(0)  # set all values below 400 to 0
threshold.ReplaceOutOn()
threshold.SetOutValue(1)  # set all values above 400 to 1
threshold.Update()

ArrayDicom = vtkImageToNumPy(threshold.GetOutput(), ConstPixelDims)
plotHeatmap(numpy.rot90(ArrayDicom[:, :, 0]), name="CT_Thresholded")

dmc = vtk.vtkDiscreteMarchingCubes()
dmc.SetInputConnection(threshold.GetOutputPort())
dmc.GenerateValues(1, 1, 1)
dmc.Update()
i=0

result = list()

for i in xrange(0,360, 1):

    # pyplot.imsave ('./COU_img2/im-%d.jpg' %i, ArrayDicom[i,:,:], cmap=pyplot.cm.bone)
    a = cv2.imread('./COU_GAP/im-%d.jpg' %i, 0)
    a=cv2.threshold(a,180,255,cv2.THRESH_BINARY)
    struct2 = ndimage.generate_binary_structure(2, 2)
    # a= ndimage.binary_dilation(a, structure=struct2).astype(a.dtype)
    # a= ndimage.binary_dilation(a, structure=struct2).astype(a.dtype)
    # a= ndimage.binary_erosion(a, structure=numpy.ones((1,1))).astype(a.dtype)
    # a= ndimage.binary_erosion(a, structure=numpy.ones((2,1))).astype(a.dtype)
    a= ndimage.binary_erosion(a, structure=numpy.ones((3,3))).astype(a.dtype)
    # a= ndimage.binary_erosion(a, structure=numpy.ones((3,2))).astype(a.dtype)
    a= ndimage.binary_dilation(a, structure=struct2).astype(a.dtype)
    a= ndimage.binary_erosion(a, structure=numpy.ones((1,1))).astype(a.dtype)
    a= ndimage.binary_dilation(a, structure=struct2).astype(a.dtype)


    # a= ndimage.binary_erosion(a, structure=numpy.ones((1,1))).astype(a.dtype)

    pyplot.imsave ('./COU_GAP/im-%d.jpg' %i, a , cmap=pyplot.cm.bone)

    # result.append(gap_reconstruction_func("./COU_img/im-%d.jpg" %i))

# for i in xrange(78,81,1):
#     pyplot.imsave ('./COU_img/im-%d.jpg' %i, ArrayDicom[:,:,i], cmap=pyplot.cm.bone)
#     a= cv2.imread('./COU_img/im-%d.jpg' %i, 0)
#     gap_reconstruction_func(ndimage.binary_erosion(a).astype(a.dtype))
#       ndimage.binary_dilation(a, structure=struct2).astype(a.dtype)
#     ndimage.binary_erosion(a, structure=numpy.ones((5,5))).astype(a.dtype)

# gap_reconstruction_func("./COU_img/im-79.jpg")