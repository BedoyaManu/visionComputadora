import cv2
import numpy as np

ix = np.array([0, 0, 0])
iy = np.array([0, 0, 0])
m = 0

def recortar(event, x, y, flags, param):
    global m, ix, iy
    if event == cv2.EVENT_LBUTTONDOWN:
        ix[m] = x
        iy[m] = y
        m += 1

