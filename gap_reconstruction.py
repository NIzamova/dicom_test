import numpy
from IPython.lib import kernel
from matplotlib import pyplot
from scipy import ndimage
import math
import cv2
from sympy import Point
import numpy.polynomial.polynomial as poly



def gap_reconstruction_func(img, a):
#     a = cv2.imread(img, 0)
#     kernel = numpy.ones((5,5),numpy.uint8)
#     a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, kernel)
#
# #find contours
#     a_canny=cv2.Canny(a, 100, 200)
#
# #
#     ret,thresh = cv2.threshold(a_canny,127,255,0)
#     im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
#     cnt = contours[0]
#     # print cnt
#     (x,y),radius = cv2.minEnclosingCircle(cnt)
#     center = (int(x),int(y))
#     radius = int(radius)
#     cv2.circle(a_canny,center,radius,(85),2)
#     cv2.imshow('ss', a_canny)
#     cv2.waitKey(0)
#
#     print(center)
#     area = cv2.contourArea(cnt)
#     perimeter = cv2.arcLength(cnt,True)
#     metric = 4*math.pi*area/perimeter**2
#     print metric
#
#     if metric<0.8:


        centerPoint=ndimage.measurements.center_of_mass(a)
        centerPoint=Point(int(centerPoint[0]), int(centerPoint[1]))
        # centerPoint=Point(center[0], center[1])
        print(centerPoint)
        print numpy.nonzero(a)




        contour_list_inner = list()
        contour_list_outer = list()
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
        for alfa in xrange(0, 361):
            alfa=alfa
            for r in xrange(0, radius):
                point_y = int(centerPoint.y+r*math.sin(math.radians(alfa)))
                point_x = int(centerPoint.x+r*math.cos(math.radians(alfa)))
                if (a[point_x, point_y]):
                    if alfa==0:
                        count_point_previous = 1
                    if count_point_previous == 0:
                        if len(gap_angle_list)==0 or abs(gap_angle_list[-1][0] - (alfa)) > 5:
                            gap_angle_list.append([alfa, str("gap end")])
                    count_point = (count_point+1)


                    if len(contour_list_inner)==0 or contour_list_inner[-1][2]!=alfa:
                        contour_list_inner.append([point_x, point_y, alfa])
                    else:
                         if len(contour_list_outer)==0 or contour_list_outer[-1][2]!=alfa:
                              contour_list_outer.append([point_x, point_y, alfa])
                         else:
                              contour_list_outer[-1]=[point_x, point_y, alfa]

                    count_point_previous = count_point


            if count_point == 0:
                if count_point_previous!=0 and alfa!=0:
                    if len(gap_angle_list)==0 or abs(gap_angle_list[-1][0] - (alfa-1)) > 5:
                        gap_angle_list.append([alfa-1, str("gap begin")])
                    count_point_previous=0
            count_point = 0


        if len(gap_angle_list)<=1:
            if len(gap_angle_list)==0:
                print str("gap not found: "+img)
            else:
                print str("very small gap: "+img)
            return



        # set alfa for regression +- 20 degrees and set m

        for alfa, stat in gap_angle_list:
            print alfa, stat

        if gap_angle_list[0][1] == "gap end":
            tmp=gap_angle_list[0][0]
            tmp2=gap_angle_list[1][0]

            gap_angle_list[0][0]= tmp2
            gap_angle_list[1][0]= 360 + tmp

        alfa_beg_for_polyfit=gap_angle_list[0][0]-30
        alfa_end_for_polyfit=gap_angle_list[1][0]+30

        for alfa, stat in gap_angle_list:
            print alfa, stat
            for r in xrange(0, radius):
                point_y = int(centerPoint.y+r*math.sin(math.radians(alfa)))
                point_x = int(centerPoint.x+r*math.cos(math.radians(alfa)))
                if (a[point_x, point_y]):
                    gap_borderline_list.append([point_x, point_y])





        # for (x,y) in gap_borderline_list:
           # print x, y





        def polyfit_draw(contour_list):
            standart_y = numpy.asarray([x for x, y, alfa in contour_list if (alfa<alfa_end_for_polyfit and alfa>alfa_beg_for_polyfit) or (alfa+360<alfa_end_for_polyfit and alfa+360>alfa_beg_for_polyfit)], dtype=numpy.int32)
            standart_x = numpy.asarray([y for x, y, alfa in contour_list if (alfa<alfa_end_for_polyfit and alfa>alfa_beg_for_polyfit) or (alfa+360<alfa_end_for_polyfit and alfa+360>alfa_beg_for_polyfit)], dtype=numpy.int32)


            if (math.sin(math.radians(alfa_beg_for_polyfit))>0  and math.sin(math.radians(alfa_end_for_polyfit))>0) or (math.sin(math.radians(alfa_beg_for_polyfit))<=0  and math.sin(math.radians(alfa_end_for_polyfit))<=0):
                aa = numpy.asarray([x for x, y in gap_borderline_list])
                x_new = numpy.arange(min(aa), max(aa), 1)
                coefs = poly.polyfit(standart_y, standart_x, 3)
                ffit = poly.polyval(x_new, coefs)
                [pyplot.plot(ffit, x_new, '-b')]
                result=[ffit, x_new, standart_x, standart_y]



            else:
                aa = numpy.asarray([y for x, y in gap_borderline_list])
                x_new = numpy.arange(min(aa), max(aa), 1)
                coefs = poly.polyfit(standart_x, standart_y, 3)
                ffit = poly.polyval(x_new, coefs)
                # [pyplot.plot(x_new, ffit, '-b')]
                result=[x_new, ffit, standart_x, standart_y]

            return result



        inner=polyfit_draw(contour_list_inner)
        outer=polyfit_draw(contour_list_outer)
        [pyplot.plot(inner[0], inner[1], '-b')]
        [pyplot.plot(outer[0], outer[1], '-b')]
        pyplot.plot(inner[2],inner[3], 'g')
        pyplot.plot(outer[2],outer[3], 'g')

        #
        # xxx = numpy.asarray([x for x, y in nonzero])
        # yyy = numpy.asarray([y for x, y in nonzero])
        # pyplot.plot(yyy, xxx, 'r')

        # pyplot.plot(standart_x,standart_y, 'g')
        # pyplot.plot(centerPoint.x, centerPoint.y, 'x')


        # print result

        pyplot.show()
        return inner[0], inner[1], outer[0], outer[1]


# Path = "./pos_jpg/pos-102.jpg"
# gap_reconstruction_func(Path)