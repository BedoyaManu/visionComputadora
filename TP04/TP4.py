import cv2
import numpy as np

ix, iy = -1, -1 
fx, fy = -1, -1

img = cv2.imread('original.jpg')
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
    
cv2.namedWindow('Imagen')
cv2.setMouseCallback('Imagen', recortar)

while True:
    cv2.imshow('Imagen', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('g'):
        if recorte:
            x0 = min(ix, fx)
            x1 = max(ix, fx)
            y0 = min(iy, fy)
            y1 = max(iy, fy)
            imgRecortada = img[y0:y1, x0:x1]
            cv2.imwrite('recorte.jpg', imgRecortada)
            break
        else:
            print("Realice un recorte primero")

    elif k == ord('q'):
        break

cv2.destroyAllWindows()