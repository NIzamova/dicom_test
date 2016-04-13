import numpy as np
import cv2
import time
from matplotlib import pyplot

im = cv2.imread('./test_neg/neg-100.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
i=0
pyplot.imsave('./test_neg/neg-100_contours.jpg', im2, cmap=pyplot.cm.bone)

print hierarchy
print hierarchy[0][0][1]
time.sleep(1)

cv2.imshow('d', im2)
cv2.waitKey(0)



im = cv2.imread('./test_pos/pos-100.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
# ret,thresh = cv2.threshold(imgray,255,255,255)
ret,thresh = cv2.threshold(imgray,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
i=0
pyplot.imsave('./test_neg/pos-100_contours.jpg', im2, cmap=pyplot.cm.bone)


print hierarchy
print hierarchy[0][0][1]
time.sleep(1)


cv2.imshow('dd', im2)
cv2.waitKey(0)

# for i in contours:
#     if (hierarchy[0][0][i] <0):
#         print "open "+ i
#
