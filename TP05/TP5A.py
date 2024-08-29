import cv2
import numpy as np

def trEucl(img, center, angle, x, y):
    (h, w) = img.shape[:2]

    if center is None:
        center = (w/2, h/2)
    
    R = cv2.getRotationMatrix2D(center, angle, 1)

    rotated = cv2.warpAffine(img, R, (w, h))

    T = np.float32([[1, 0, x], [0, 1, y]])

    transformed = cv2.warpAffine(rotated, T, (w, h))
    
    return transformed

img = cv2.imread('original.jpg')

tx = int(input('Introduzca la translación en x: '))
ty = int(input('Introduzca la translación en y: '))
angle = float(input('Introduzca el ángulo de rotación: '))

transformed = trEucl(img, None, angle, tx, ty)

cv2.namedWindow('Imagen')
cv2.imshow('Imagen', transformed)
cv2.waitKey(0)
cv2.destroyAllWindows()