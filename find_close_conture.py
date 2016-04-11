import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

im = cv2.imread('./test_pos/pos-80.png')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
i=0

print hierarchy
if (hierarchy[0][2] <0):
    print "open "+ i

