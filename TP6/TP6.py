import cv2
import numpy as np

ix, iy = -1, -1 
fx, fy = -1, -1

recorte = False

def recortar(event, x, y, flags, param):
    global ix, iy, fx, fy, img, recorte
    if event == cv2.EVENT_LBUTTONDOWN:
        ix , iy = x, y
        img = cv2.imread('original.jpg')
    elif event == cv2.EVENT_LBUTTONUP:
        cv2.rectangle(img, (ix, iy), (x, y), (255, 0, 0), 0)
        recorte = True
        fx = x
        fy = y


def trEucl(img, center, angle, x, y, scale):
    (h, w) = img.shape[:2]

    if center is None:
        center = (w/2, h/2)
    
    R = cv2.getRotationMatrix2D(center, angle, scale)

    rotated = cv2.warpAffine(img, R, (w, h))

    T = np.float32([[1, 0, x], [0, 1, y]])

    transformed = cv2.warpAffine(rotated, T, (w, h))
    
    return transformed

img = cv2.imread('original.jpg')
cv2.namedWindow('Imagen')
cv2.setMouseCallback('Imagen', recortar)

while True:
    cv2.imshow('Imagen', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('e'):
        if recorte:
            x0 = min(ix, fx)
            x1 = max(ix, fx)
            y0 = min(iy, fy)
            y1 = max(iy, fy)
            imgRecortada = img[y0:y1, x0:x1]
            tx = int(input('Introduzca la translación en x: '))
            ty = int(input('Introduzca la translación en y: '))
            angle = float(input('Introduzca el ángulo de rotación: '))
            scale = float(input('Introduzca la escala deseada: '))
            transformed = trEucl(imgRecortada, None, angle, tx, ty, scale)

            cv2.imshow('Imagen', transformed)
            cv2.waitKey(0)
            cv2.imwrite('transformada.jpg',transformed)
            break
        else:
            print('Seleccione una parte de la imagen primero')
    
    elif k == 27:
        break

cv2.destroyAllWindows()