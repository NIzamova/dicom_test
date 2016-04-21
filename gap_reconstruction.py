import numpy
from matplotlib import pyplot
from scipy import ndimage
import math
import cv2
from sympy import Point

Path = "./pos_jpg/pos-100.jpg"

a = cv2.imread(Path, 0)
nonzero = numpy.transpose(numpy.nonzero(a))


centerPoint=ndimage.measurements.center_of_mass(a)
centerPoint=Point(int(centerPoint[0]), int(centerPoint[1]))
print(centerPoint)


contur_list = list()
gap_borderline_list = list()
gap_angle_list = list()
count_point = 0
radius_begin = 1
count_point_previous = 0

# TODO for 45, 135, 225, 315 degrees theirself alfa
radius = min([centerPoint.x, centerPoint.y, 512-centerPoint.x, 512-centerPoint.y])


# find gap's begin and gap's end
# contour_list - point of skull (x, y, alfa)
# gap_angle_list - alfa and status(begin/end)
# count_point and count_point_previous help to find gap's begin and end
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

    if count_point == 0:
        if count_point_previous!=0 and alfa!=0:
            gap_angle_list.append([alfa-1, str("gap begin")])
            count_point_previous=0
    count_point = 0



# set alfa for regression +- 20 degrees
for alfa, stat in gap_angle_list:
    print alfa, stat
    if stat == "gap begin":
        alfa_beg_for_polyfit=alfa-20
    else:
        alfa_end_for_polyfit=alfa+20

    for r in xrange(0, radius):
        point_y = int(centerPoint.y+r*math.sin(math.radians(alfa)))
        point_x = int(centerPoint.x+r*math.cos(math.radians(alfa)))
        if (a[point_x, point_y]):
            gap_borderline_list.append([point_x, point_y])




for (x,y) in gap_borderline_list:
   print x, y


standart_y = numpy.asarray([x for x, y, alfa in contur_list if alfa<alfa_end_for_polyfit and alfa>alfa_beg_for_polyfit], dtype=numpy.int32)
standart_x = numpy.asarray([y for x, y, alfa in contur_list if alfa<alfa_end_for_polyfit and alfa>alfa_beg_for_polyfit], dtype=numpy.int32)

print (gap_borderline_list[:])

import numpy.polynomial.polynomial as poly
x_new = numpy.arange(min(gap_borderline_list[:][0]), max(gap_borderline_list[:][0]), 1)
coefs = poly.polyfit(standart_x, standart_y, 3)
ffit = poly.polyval(x_new, coefs)
print x_new, ffit
pyplot.plot(x_new, ffit)
pyplot.plot(standart_x,standart_y, 'g')


pyplot.show()


