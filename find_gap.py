import numpy
from IPython.lib import kernel
from matplotlib import pyplot
from scipy import ndimage
import math
import cv2
from sympy import Point
import numpy.polynomial.polynomial as poly
from gap_reconstruction import gap_reconstruction_func



def find_gap(img):
    a = cv2.imread(img, 0)
    kernel = numpy.ones((5,5),numpy.uint8)
    a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, kernel)

#find contours
    a_canny=cv2.Canny(a, 100, 200)

#
    ret,thresh = cv2.threshold(a_canny,127,255,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    # print cnt
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)
    cv2.circle(a_canny,center,radius,(85),2)
    cv2.imshow('ss', a_canny)
    cv2.waitKey(0)

    print(center)
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt,True)
    metric = 4*math.pi*area/perimeter**2
    print metric

    if metric<0.8:
        gap=gap_reconstruction_func(img, a)
        print str('GAP FIND ')
        a_canny[gap[1].astype(int),gap[0].astype(int)] = 255
        a_canny[gap[3].astype(int),gap[2].astype(int)] = 255
        cv2.imshow('jjj', a_canny)
        cv2.waitKey(0)


    return gap