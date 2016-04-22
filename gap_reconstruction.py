import numpy
from matplotlib import pyplot
from scipy import ndimage
import math
import cv2
from sympy import Point
import numpy.polynomial.polynomial as poly

# Path = "./pos_jpg/pos-112.jpg"


def gap_reconstruction_func(img):
    a = cv2.imread(img, 0)
    # a = img
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
                    if len(gap_angle_list)==0 or abs(gap_angle_list[-1][0] - (alfa)) > 3:
                        gap_angle_list.append([alfa, str("gap end")])

                count_point = (count_point+1)
                contur_list.append([point_x, point_y, alfa])
                count_point_previous = count_point


        if count_point == 0:
            if count_point_previous!=0 and alfa!=0:
                if len(gap_angle_list)==0 or abs(gap_angle_list[-1][0] - (alfa-1)) > 3:
                    gap_angle_list.append([alfa-1, str("gap begin")])
                count_point_previous=0
        count_point = 0


    if len(gap_angle_list)==0:
        print str("gap not found")
        return



    # set alfa for regression +- 20 degrees and set m

    for alfa, stat in gap_angle_list:
        print alfa, stat

    if gap_angle_list[0][1] == "gap end":
        tmp=gap_angle_list[0][0]
        tmp2=gap_angle_list[1][0]

        gap_angle_list[0][0]= tmp2
        gap_angle_list[1][0]= 360 + tmp

    alfa_beg_for_polyfit=gap_angle_list[0][0]-20
    alfa_end_for_polyfit=gap_angle_list[1][0]+20

    for alfa, stat in gap_angle_list:
        print alfa, stat
        for r in xrange(0, radius):
            point_y = int(centerPoint.y+r*math.sin(math.radians(alfa)))
            point_x = int(centerPoint.x+r*math.cos(math.radians(alfa)))
            if (a[point_x, point_y]):
                gap_borderline_list.append([point_x, point_y])




    for (x,y) in gap_borderline_list:
       print x, y


    standart_y = numpy.asarray([x for x, y, alfa in contur_list if (alfa<alfa_end_for_polyfit and alfa>alfa_beg_for_polyfit) or (alfa+360<alfa_end_for_polyfit and alfa+360>alfa_beg_for_polyfit)], dtype=numpy.int32)
    standart_x = numpy.asarray([y for x, y, alfa in contur_list if (alfa<alfa_end_for_polyfit and alfa>alfa_beg_for_polyfit) or (alfa+360<alfa_end_for_polyfit and alfa+360>alfa_beg_for_polyfit)], dtype=numpy.int32)


    if (alfa_beg_for_polyfit>0 and alfa_beg_for_polyfit<=180 and alfa_end_for_polyfit>0 and alfa_end_for_polyfit<=180) or (alfa_beg_for_polyfit>180 and alfa_beg_for_polyfit<=360 and alfa_end_for_polyfit>180 and alfa_end_for_polyfit<=360) or (alfa_beg_for_polyfit>360 and alfa_beg_for_polyfit<=540 and alfa_end_for_polyfit>360 and alfa_end_for_polyfit<=540):
        aa = numpy.asarray([x for x, y in gap_borderline_list])
        x_new = numpy.arange(min(aa), max(aa), 1)
        coefs = poly.polyfit(standart_y, standart_x, 3)
        ffit = poly.polyval(x_new, coefs)
        [pyplot.plot(ffit, x_new, '-b')]
        result=[ffit.astype(int), x_new.astype(int)]



    else:
        aa = numpy.asarray([y for x, y in gap_borderline_list])
        x_new = numpy.arange(min(aa), max(aa), 1)
        coefs = poly.polyfit(standart_x, standart_y, 3)
        ffit = poly.polyval(x_new, coefs)
        [pyplot.plot(x_new, ffit, '-b')]
        result=[x_new.astype(int), ffit.astype(int)]

    #
    # xxx = numpy.asarray([x for x, y in nonzero])
    # yyy = numpy.asarray([y for x, y in nonzero])
    # pyplot.plot(yyy, xxx, 'r')

    pyplot.plot(standart_x,standart_y, 'g')
    # pyplot.plot(centerPoint.x, centerPoint.y, 'x')


    print result

    # pyplot.show()
    return result


