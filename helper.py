
from scipy import ndimage


import dicom, dicom.UID
import matplotlib
import numpy as np
from matplotlib import pyplot
import cv2


# for i in xrange(80,81, 1):

    # ds = dicom.read_file("./COU/IM-0001-00%d.dcm" %i)

    #
    # pyplot.imshow('dd', ds.pixel_array, cmap=pyplot.cm.bone)
    # pyplot.show()

for i in xrange(76,77, 1):

    # pyplot.imsave ('./COU_img2/im-%d.jpg' %i, ArrayDicom[i,:,:], cmap=pyplot.cm.bone)
    # a = pyplot.imread('./COU_GAP/im-%d.jpg' %i, 0)
    # a=cv2.threshold(a,180,255,cv2.THRESH_BINARY)
    # cv2.imshow('dd', a)
    # cv2.waitKey(0)

    a = cv2.imread('./COU_GAP/im-%d.jpg' %i, 0)
    a=cv2.flip(a, 0)
    # kernel = np.ones((5,5),np.uint8)
    # a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, kernel)
    # a = cv2.morphologyEx(a, cv2.MORPH_OPEN, kernel)



    # a=cv2.threshold(a,180,255,cv2.THRESH_BINARY)
    # struct2 = ndimage.generate_binary_structure(2, 2)
    # a= ndimage.binary_dilation(a, structure=struct2).astype(a.dtype)
    # a= ndimage.binary_dilation(a, structure=struct2).astype(a.dtype)
    # a= ndimage.binary_erosion(a, structure=numpy.ones((1,1))).astype(a.dtype)
    # a= ndimage.binary_erosion(a, structure=numpy.ones((2,1))).astype(a.dtype)
    # a= ndimage.binary_erosion(a, structure=np.ones((3,3))).astype(a.dtype)
    # a= ndimage.binary_erosion(a, structure=numpy.ones((3,2))).astype(a.dtype)
    # a= ndimage.binary_dilation(a, structure=struct2).astype(a.dtype)
    # a= ndimage.binary_erosion(a, structure=np.ones((1,1))).astype(a.dtype)
    # a= ndimage.binary_dilation(a, structure=struct2).astype(a.dtype)


    # a= ndimage.binary_erosion(a, structure=numpy.ones((1,1))).astype(a.dtype)

    pyplot.imsave ('./COU_GAP/im-%d.jpg' %i, a , cmap=pyplot.cm.bone)
