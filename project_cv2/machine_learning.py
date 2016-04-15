import os

import numpy as np
import cv2
from matplotlib import pyplot

Path = "./test_validation/"
for dirname, dirnames, filenames in os.walk(Path):
    for filename in filenames:
        print filename
        hall_cascade = cv2.CascadeClassifier('cascade.xml')
        img = cv2.imread(os.path.join(dirname, filename))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = hall_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            print x , y
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

        cv2.imshow('img', img)
        cv2.waitKey(0)

        pyplot.imsave('./test_validation_result/%s.jpg' %filename, img, cmap=pyplot.cm.bone)
        print(roi_gray)