import random
import numpy
import cv2
import dicom
from matplotlib import pyplot
from matplotlib._image import Image

Path = "./test_pos/"
w = 180
h = 180

ds = dicom.read_file("./IM-0001-0400.dcm")
nRows = ds.Rows;
nCols = ds.Columns;
nPlanes = ds.SamplesPerPixel;
nFrames = 1;


a=(ds.pixel_array>1400)
# pyplot.imshow(a)
# pyplot.show()
nonzerot = numpy.transpose(numpy.nonzero(a))
nonzero = numpy.nonzero(a)
s= nonzerot.size/2
training_dataset_list = list()
i = 0
for(x,y) in nonzerot:
    print x, y

for (x,y) in nonzerot[xrange(1, s, 30)]:
    ab = a.astype(int)
    r_out=int(random.randint(100, 280)/2)
    r_in=int(r_out/3)
    i=i+1
    xStart_out=x-r_out
    yStart_out=y-r_out
    xEnd_out=x+r_out
    yEnd_out=y+r_out
    if (xStart_out<0):
            xStart_out = 0
    if (yStart_out<0):
            yStart_out=0
    if (xEnd_out>511):
            xEnd_out=511
    if (yEnd_out>511):
            yEnd_out=511;

    frame_out = ab[xStart_out:xEnd_out, yStart_out:yEnd_out]

    xStart_in = x-r_in
    xEnd_in = x+r_in
    yStart_in = y-r_in
    yEnd_in = y+r_in

    if (xStart_in<0):
            xStart_out = 0
    if (yStart_in<0):
            yStart_out=0
    if (xEnd_in>511):
            xEnd_out=511
    if (yEnd_in>511):
            yEnd_out=511;
    ab[xStart_in:xEnd_in, yStart_in:yEnd_in] = 0
    filename = str("./training_dataset/pos-0001-0400-%d.jpg" %i)
    # im = Image.fromarray(ab)
    # im.save(filename)
    pyplot.imsave(filename,ab, cmap=pyplot.cm.bone)
    training_dataset_list.append([filename,yStart_out,xStart_out,r_out*2] )


openfile = open("./training_dataset/training_dataset_list.dat", 'w')
for j in xrange(i):
    openfile.write(str(training_dataset_list[j][0]) + " " + str("1")+ " " + str(training_dataset_list[j][1]) + " " + str(training_dataset_list[j][2]) + " " + str(training_dataset_list[j][3]) + " " +str(training_dataset_list[j][3]) +"\n")
openfile.close()

# pyplot.imshow(ab, cmap=pyplot.cm.bone)
# pyplot.show()