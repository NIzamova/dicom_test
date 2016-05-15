from dicom.dataset import Dataset, FileDataset
import numpy as np
import datetime, time
import matplotlib
matplotlib.use('TkAgg')
from mpl_toolkits.mplot3d import Axes3D

import os
import random
import numpy
import cv2
import dicom
from matplotlib import pyplot
from matplotlib._image import Image
from scipy import ndimage
from sympy import Point
from matplotlib import cm


from find_gap import find_gap


def write_dicom(pixel_array,filename):
    """
    INPUTS:
    pixel_array: 2D numpy ndarray.  If pixel_array is larger than 2D, errors.
    filename: string name for the output file.
    """

    ## This code block was taken from the output of a MATLAB secondary
    ## capture.  I do not know what the long dotted UIDs mean, but
    ## this code works.
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = 'Secondary Capture Image Storage'
    file_meta.MediaStorageSOPInstanceUID = '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
    file_meta.ImplementationClassUID = '1.3.6.1.4.1.9590.100.1.0.100.4.0'
    ds = FileDataset(filename, {},file_meta = file_meta,preamble="\0"*128)
    ds.Modality = 'WSD'
    ds.ContentDate = str(datetime.date.today()).replace('-','')
    ds.ContentTime = str(time.time()) #milliseconds since the epoch
    ds.StudyInstanceUID =  '1.3.6.1.4.1.9590.100.1.1.124313977412360175234271287472804872093'
    ds.SeriesInstanceUID = '1.3.6.1.4.1.9590.100.1.1.369231118011061003403421859172643143649'
    ds.SOPInstanceUID =    '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
    ds.SOPClassUID = 'Secondary Capture Image Storage'
    ds.SecondaryCaptureDeviceManufctur = 'Python 2.7.3'

    ## These are the necessary imaging components of the FileDataset object.
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 0
    ds.HighBit = 15
    ds.BitsStored = 16
    ds.BitsAllocated = 16
    ds.SmallestImagePixelValue = '\\x00\\x00'
    ds.LargestImagePixelValue = '\\xff\\xff'
    ds.Columns = pixel_array.shape[0]
    ds.Rows = pixel_array.shape[1]
    if pixel_array.dtype != numpy.uint16:
        pixel_array = pixel_array.astype(numpy.uint16)
    ds.PixelData = pixel_array.tostring()

    ds.save_as(filename)
    return




result = list()
Path="./COU_GAP/"
N=512



for i in xrange(31, 91,1):
    print str("./COU_GAP/IM-%d.jpg" %i)
    ds = dicom.read_file("./COU/IM-0001-00%d.dcm" %i)
    result_2d= numpy.zeros((512, 512))
    result_2d.astype(int)

    a= pyplot.imread("./COU_GAP/IM-%d.jpg" %i)
    gap=find_gap("./COU_GAP/im-%d.jpg" %i)
    if gap==0:
        gap=find_gap("./COU_GAP/im-%d.jpg" %(i-1))
    if gap=="SLIDE WITHOUT GAP":
        continue

    # pa=ds.pixel_array

    result_2d[gap[0].astype(int),gap[1].astype(int)]=int(2000)
    result_2d[gap[2].astype(int),gap[3].astype(int)]=int(2000)

    openfile = open('LOOKHERE.txt', 'w')
    openfile.write(str((a)) + "\n")
    openfile.close()
    if result_2d.dtype != np.uint16:
        result_2d = result_2d.astype(np.uint16)
    ds.PixelData = result_2d.tostring()

    ds.save_as("./COU_GAP/papka/im-%d.dcm" %i )
    # write_dicom(a,"./COU_GAP/im-%d.dcm" %i )


    # fig = pyplot.figure()
    # ax = fig.gca( projection='3d')
    # X=gap[0]
    # Y=gap[1]
    # Z=i
    # X, Y = np.meshgrid(X, Y)
    #
    # ax.plot_surface(X, Y, Z)
    # pyplot.show()




