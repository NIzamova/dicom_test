from time import time

#from plotly.js import Heatmap as Heatmap
from IPython.core.display import display
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly.graph_objs import *
import plotly

init_notebook_mode()
from IPython.display import Image
__author__ = 'N'
import dicom
import os
import numpy
import vtk
import matplotlib
from vtk.util import numpy_support
from matplotlib import pyplot
import third

import numpy
from stl import mesh

#plotly.plotly.sign_in("liliya", "4m3yij5fes") #"liliya_liliya")


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


 #   plotly.plotly.image.save_as(fig, filename='test_name.png')
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
#
# shiftScale = vtk.vtkImageShiftScale()
# shiftScale.SetScale(reader.GetRescaleSlope())
# shiftScale.SetShift(reader.GetRescaleOffset())
# shiftScale.SetInputConnection(reader.GetOutputPort())
# shiftScale.Update()

threshold = vtk.vtkImageThreshold ()
threshold.SetInputConnection(reader.GetOutputPort())
threshold.ThresholdByLower(400)  # remove all soft tissue
threshold.ReplaceInOn()
threshold.SetInValue(0)  # set all values below 400 to 0
threshold.ReplaceOutOn()
threshold.SetOutValue(1)  # set all values above 400 to 1
threshold.Update()

ArrayDicom = vtkImageToNumPy(threshold.GetOutput(), ConstPixelDims)
# print type(ArrayDicom)
plotHeatmap(numpy.rot90(ArrayDicom[:, :, 0]), name="CT_Thresholded")

# print(time())
dmc = vtk.vtkDiscreteMarchingCubes()
dmc.SetInputConnection(threshold.GetOutputPort())
dmc.GenerateValues(1, 1, 1)
dmc.Update()
i=0
for i in xrange(361):
    third.start_ray(pyplot.imshow ('./COU/neg-%d.png' %i, ArrayDicom[:,:,i]), i)
    # nonzero = numpy.transpose(numpy.nonzero(ArrayDicom[:,:,i]))
    # for (x,y) in nonzero:
    #     print x, y
     # pyplot.set_cmap(pyplot.cm.bone)
     # pyplot.imshow ('./COU/neg-%d.png' %i, ArrayDicom[:,:,i])
     # pyplot.show()

    # pyplot.imsave('./COU_img/im-%d.png' %i, ArrayDicom[:,:,i], cmap=pyplot.cm.bone)
print(ArrayDicom)
#
#
# mapper = vtk.vtkPolyDataMapper()
# mapper.SetInputConnection(dmc.GetOutputPort())
#
# actor = vtk.vtkActor()
# actor.SetMapper(mapper)
#
# renderer = vtk.vtkRenderer()
# renderer.AddActor(actor)
# renderer.SetBackground(1.0, 1.0, 1.0)
#
# camera = renderer.MakeCamera()
# camera.SetPosition(-500.0, 245.5, 122.0)
# camera.SetFocalPoint(301.0, 245.5, 122.0)
# camera.SetViewAngle(30.0)
# camera.SetRoll(-90.0)
# renderer.SetActiveCamera(camera)
#
# display(vtk_show(renderer, 600, 600))
# pyplot.show()
#from IPython.display import Image
#Image('test_name.pmg')
#
# writer = vtk.vtkSTLWriter()
# writer.SetInputConnection(dmc.GetOutputPort())
# writer.SetFileTypeToBinary()
# writer.SetFileName("lite_bones.stl")
# writer.Write()

