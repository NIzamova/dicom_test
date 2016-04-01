import numpy, dicom, os
import pylab
from matplotlib import pyplot, cm
from numpy.matlib import repmat
from scipy import ndimage
import math

from sympy import Point

PathDicom = "./lite/"

ds = dicom.read_file("./lite/IM-0001-0450.dcm")
nRows = ds.Rows;
nCols = ds.Columns;
nPlanes = ds.SamplesPerPixel;
nFrames = 1;

pix = ds.pixel_array

for n,val in enumerate(ds.pixel_array.flat):
    if val < 2000:
        ds.pixel_array.flat[n]=0
ds.PixelData = ds.pixel_array
a=ds.PixelData
centerPoint=ndimage.measurements.center_of_mass(a)
centerPoint=Point(int(centerPoint[0]), int(centerPoint[1]))
print(centerPoint)

def isBetween(a, b, c):
    epsilon =0.0001
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)
    if abs(crossproduct) > epsilon : return False   # (or != 0 if using integers)

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
    if dotproduct < 0 : return False

    squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
    if dotproduct > squaredlengthba: return False

    return True

count = 0
value=1
angle = (math.pi / 180) * value;
p = Point(512, 512)

while angle <1:
    for (x,y), value in numpy.ndenumerate(a):
            if  a[x,y] != 0:
                endpoint = Point(x, y)
                if isBetween(centerPoint, p, endpoint):
                    count= count +1
                    print(x,y)
value= value +1
angle = (math.pi / 180) * value;
p.x1 = ((p.x * math.acos(angle)) + (p.y * math.asin(angle)));
p.y1 = -((p.x * math.asin(angle)) + (p.y * math.acos(angle)));
p.x=p.x1
p.y=p.y1






#ds.save_as("newfilename.dcm")
# pylab.imshow(ds.PixelData, cmap=pylab.cm.bone)
# pylab.show()


# openfile = open('LOOKHERE.txt', 'w')
# for item in ds.PixelData:
#     openfile.write(str(item) + "\n")
# openfile.close()

