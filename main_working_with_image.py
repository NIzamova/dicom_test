import os
import random
import numpy
import cv2
import dicom
from matplotlib import pyplot
from matplotlib._image import Image
from scipy import ndimage

from gap_reconstruction import gap_reconstruction_func

result = list()
Path="./COU_GAP/"

for i in xrange(70,90,1):
    a= pyplot.imread("./COU_GAP/im-%d.jpg" %i)
    # print("./COU_GAP/im-%d.jpg" %i)
    # pyplot.imshow(a)
    # pyplot.show()
    # a= ndimage.binary_erosion(a, structure=numpy.ones((1,1))).astype(a.dtype)
    result.append(gap_reconstruction_func("./COU_GAP/im-%d.jpg" %i))
print result