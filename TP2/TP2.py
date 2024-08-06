import cv2
import numpy as np

img = cv2.imread('original.jpg' , 0)

dimensions = img.shape

for i in range(dimensions[0]):
    for j in range(dimensions[1]):
        if img[i,j] < 128:
            img[i,j] = 0
        else:
            img[i,j] = 255

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows

cv2.imwrite('resultado.jpg', img)