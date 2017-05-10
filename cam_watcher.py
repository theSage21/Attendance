import os
from scipy.misc import imresize
import numpy as np
import cv2

names = os.listdir('haar')
cascades = [cv2.CascadeClassifier('haar/'+name) for name in names]

cap = cv2.VideoCapture(0)

facecuts = []
while True:
    ret, img = cap.read()
    if ret:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        for face_cascade in cascades:
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            for (x, y, w, h) in faces:
                facecuts.append(img[y:y+h, x:x+w].copy())
        if len(facecuts) > 0:
            a = min(i.shape[0] for i in facecuts)
            b = min(i.shape[1] for i in facecuts)
        newfaces = [imresize(i, (a, b, 3)) for i in facecuts]
        display = np.concatenate(newfaces) if len(newfaces) > 0 else img
        cv2.imshow('img', newfaces[-1])
    if cv2.waitKey(1) & 0xFF == ord('q'):
                break
cv2.destroyAllWindows()
