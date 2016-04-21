import numpy, dicom, os
from numpy import linspace,exp
from plotly.plotly import plotly
import pylab
from matplotlib import pyplot, cm
from numpy.matlib import repmat
from scipy import ndimage
import scipy.sparse
import math
import cv2
import plotly.graph_objs as go
import matplotlib.image as mpimg
from scipy.interpolate import interp1d
from scipy.interpolate import UnivariateSpline

from sympy import Point, interpolate

# Path = "./pos_jpg/im-80.jpg"
Path = "./pos_jpg/pos-100.jpg"
# PathDicom = "./lite/"

# ds = dicom.read_file("./lite/IM-0001-0450.dcm")
# nRows = ds.Rows;
# nCols = ds.Columns;
# nPlanes = ds.SamplesPerPixel;
# nFrames = 1;
# pix = ds.pixel_array

# a=(ds.pixel_array>2000)


# pyplot.imsave('current_test.png', a, cmap=pylab.cm.bone)

a=cv2.imread(Path, 0)
# img = mpimg.imread(Path)
# a = img.set_cmap('spectral')
print a.size
print a[200, 200]
nonzero = numpy.transpose(numpy.nonzero(a))
# for (x,y) in nonzero:
#     print x, y


centerPoint=ndimage.measurements.center_of_mass(a)
centerPoint=Point(int(centerPoint[0]), int(centerPoint[1]))
print(centerPoint)

def distance(x1, x2, y1, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

contur_list = list()
gap_borderline_list = list()
gap_angle_list = list()
count_point = 0
radius_begin = 1
count_point_previous=0
# radius = (distance(centerPoint.x, nonzero[0][0],  centerPoint.y, nonzero[0][1]))
# radius_end = radius*1.2
radius =  min([centerPoint.x, centerPoint.y, 512-centerPoint.x, 512-centerPoint.y])



for alfa in xrange(0, 360):

    for r in xrange(0, radius):
        point_y = int(centerPoint.y+r*math.sin(math.radians(alfa)))
        point_x = int(centerPoint.x+r*math.cos(math.radians(alfa)))
        if (a[point_x, point_y]):
            if alfa==0:
                count_point_previous = 1
            if count_point_previous == 0:
                gap_angle_list.append([alfa, str("gap end")])

            count_point = (count_point+1)

            contur_list.append([point_x, point_y, alfa])
            count_point_previous=count_point
            # print ("in alfa = " +str(alfa)+" point found!!!!! "+str(point_x)+", " +str( point_y)+" count is " + str(count_point)+ " color is "+ str(a[point_x, point_y]))


    if count_point == 0:
        if count_point_previous!=0 and alfa!=0:
            gap_angle_list.append([alfa-1, str("gap begin")])
            count_point_previous=0
            # for i in xrange(1,count_point_previous+1):
            #     gap_borderline_list.append(contur_list[-i])


        # print ("point not found!!!!! " + str(alfa))


    count_point = 0
    # openfile = open('LOOKHERE.txt', 'w')
    # openfile.write(str((contur_list)) + "\n")
    # openfile.close()
    # print alfa


for alfa, stat in gap_angle_list:
    print alfa, stat
    if stat == "gap begin":
        alfa_beg_for_polyfit=alfa-20
    else:
        alfa_end_for_polyfit=alfa+20
    print alfa, stat
    for r in xrange(0, radius):
        point_y = int(centerPoint.y+r*math.sin(math.radians(alfa)))
        point_x = int(centerPoint.x+r*math.cos(math.radians(alfa)))
        if (a[point_x, point_y]):
            gap_borderline_list.append([point_x, point_y])




for (x,y) in gap_borderline_list:
   print x, y
# pyplot.imshow(a)
# pyplot.show()

# x = linspace(-3, 3,50)
# y = linspace(-3, 3,50)
# plotly.plot(x, y, 'ro', ms=5)
# spl = UnivariateSpline(x, y)
# xs = numpy.linspace(-3, 3, 1000)
# plotly.plot(xs, spl(xs), 'g', lw=3)
# spl.set_smoothing_factor(0.5)
# plotly.plot(xs, spl(xs), 'b', lw=3)
# plotly.show()



# x =numpy.asarray([x for x, y in contur_list], dtype=float)
# x_csr = scipy.sparse.csr_matrix(x)
# xx = scipy.sparse.dok_matrix(x.reshape(x_csr.shape[0]))
# y =numpy.asarray([y for x, y in contur_list], dtype=float)
# y_csr = scipy.sparse.csr_matrix(y)
# yy = scipy.sparse.dok_matrix(y.reshape(y_csr.shape[0]))

from scipy import interpolate

standart_y = numpy.asarray([x for x, y, alfa in contur_list if alfa<alfa_end_for_polyfit and alfa>alfa_beg_for_polyfit], dtype=numpy.int32)
standart_x = numpy.asarray([y for x, y, alfa in contur_list if alfa<alfa_end_for_polyfit and alfa>alfa_beg_for_polyfit], dtype=numpy.int32)
# f = interp1d(standart_x, standart_y)
# f2 = interp1d(standart_x, standart_y, kind='cubic')

import numpy.polynomial.polynomial as poly
x_new = numpy.arange(223, 350, 1)
coefs = poly.polyfit(standart_x, standart_y, 3)
ffit = poly.polyval(x_new, coefs)
print x_new, ffit
pyplot.plot(x_new, ffit)
pyplot.plot(standart_x,standart_y, 'g')



#
#
# tck, u = interpolate.splprep([standart_x, standart_y], s=0)
#
# unew = numpy.arange(128.0, 155.0, 1.0)
# out = interpolate.splprep(unew, tck)
# plotly.figure()
# plotly.plot( out[0], out[1],numpy.sin(2*numpy.pi*unew), numpy.cos(2*numpy.pi*unew),standart_x, standart_y, 'b' )
# plotly.show()

# xint = numpy.arange(223, 320, 1)
# m, b = numpy.polyfit(standart_x, standart_y, 3)
# pyplot.plot(standart_x,standart_y,'.')
# pyplot.plot(standart_x, standart_x*m+b, '-')


# yint = f(xint)
# pyplot.figure()
# pyplot.plot(standart_x, standart_y, '-b', xint, yint, '-g')
pyplot.show()

#
# def div(a, b):
#     try:
#         return a / float(b)
#     except ZeroDivisionError:
#         return 0
#
# def N(i, k, x, t):
#     if 1 == k:
#         if t[i] <= x < t[i + 1]:
#             return 1.0
#         return 0.0
#     a = div(x - t[i], t[i + k - 1] - t[i]) * N(i, k - 1, x, t)
#     b = div(t[i + k] - x, x[i + k] - x[i + 1]) * N(i + 1, k - 1, x, t)
#


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


