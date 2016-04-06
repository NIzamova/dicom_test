import numpy, dicom, os
from plotly.plotly import plotly
import pylab
from matplotlib import pyplot, cm
from numpy.matlib import repmat
from scipy import ndimage
import math
import plotly.graph_objs as go

from sympy import Point

PathDicom = "./lite/"

ds = dicom.read_file("./lite/IM-0001-0450.dcm")
nRows = ds.Rows;
nCols = ds.Columns;
nPlanes = ds.SamplesPerPixel;
nFrames = 1;

# pix = ds.pixel_array

a=(ds.pixel_array>2000)
# mat = numpy.where(numpy.any(a>0, axis=1))
# print mat

pyplot.imsave('current_test.png', a, cmap=pylab.cm.bone)

nonzero = numpy.transpose(numpy.nonzero(a))
for (x,y) in nonzero:
    print x, y

# for n,val in enumerate(ds.pixel_array.flat):
#     if val < 1800:
#         ds.pixel_array.flat[n]=0
#     else:
#         ds.pixel_array.flat[n]=1
# ds.PixelData = int(ab)

centerPoint=ndimage.measurements.center_of_mass(a)
centerPoint=Point(int(centerPoint[0]), int(centerPoint[1]))
print(centerPoint)

def distance(x1, x2, y1, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5
contur_list = list()
point_x = centerPoint.x
point_y = centerPoint.y
count_point =0
radius=(distance(centerPoint.x, 192,  centerPoint.y, 277))*1.5
for alfa in xrange(0, 360):
    count_point =0
    for r in xrange(1, radius):
        point_y= centerPoint.y+r*math.sin(math.radians(alfa))
        point_x= centerPoint.x+r*math.cos(math.radians(alfa))
        for (x,y) in nonzero:
              if ((x - point_x)==0 and (y - point_y)==0):
                  contur_list.append([point_x,point_y])
                  openfile = open('LOOKHERE.txt', 'w')
                  openfile.write(str((contur_list)) + "\n")
                  openfile.close()
                  count_point= (count_point+1)
                  print ("in alfa = " +str(alfa)+" point found!!!!! count is " + str(count_point))
    if count_point==0:
        contur_list.append([alfa, alfa])
        print ("point not found!!!!! " + str(alfa))
    print alfa



#ds.save_as("newfilename.dcm")
#pylab.figure()
# pyplot.imshow(int(ab), cmap=pylab.cm.bone)
# pyplot.show()
#
# openfile = open('LOOKHERE.txt', 'w')
# for item in ds.PixelData:
#      openfile.write(str(item) + "\n")
# openfile.close()
#
