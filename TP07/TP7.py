import cv2
import numpy as np

m = 0
dstPoints = []
img1 = cv2.imread('timeSquare.jpg')

def seleccionar(event, x, y, flags, param):
    global m, dstPoints, img1
    if event == cv2.EVENT_LBUTTONDOWN:
        if m == 3:
            print('Se seleccionaron más de 3 puntos, seleccione 3 nuevamente')
            m = 0
            dstPoints.clear()
            img1 = cv2.imread('timeSquare.jpg')
        dstPoints.append([x, y])
        m += 1
        cv2.circle(img1, (x, y), 2, (0, 0, 255), -1)
        cv2.imshow('img1', img1)

def trAffine(img, dstPoints, srcPoints, size):
    dstPoints = np.array(dstPoints, dtype=np.float32)
    srcPoints = np.array(srcPoints, dtype=np.float32)
    M = cv2.getAffineTransform(srcPoints, dstPoints)
    transformada = cv2.warpAffine(img, M, (size[1], size[0]))
    return transformada

def estimateFourthPoint(dstPoints):
    pt1, pt2, pt3 = dstPoints
    pt4 = [pt1[0] + (pt3[0] - pt2[0]), pt1[1] + (pt3[1] - pt2[1])]
    return pt4

def insertImage(img, imgTransf, dstPoints):
    mask = np.zeros(img.shape, dtype=np.uint8)
    pt4 = estimateFourthPoint(dstPoints)
    roi_corners = np.array([dstPoints + [pt4]], dtype=np.int32)
    cv2.fillConvexPoly(mask, roi_corners, (255, 255, 255))
    
    mask_inv = cv2.bitwise_not(mask)
    
    img_bg = cv2.bitwise_and(img, mask_inv)
    img_fg = cv2.bitwise_and(imgTransf, mask)

    result = cv2.add(img_bg, img_fg)
    return result

img2 = cv2.imread('stormTrooper.jpg')

cv2.namedWindow('img1')
cv2.setMouseCallback('img1', seleccionar)

srcPoints = np.array([[0, 0], [0, img2.shape[0]], [img2.shape[1], img2.shape[0]]], dtype=np.float32)

while True:
    cv2.imshow('img1', img1)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('a'):
        if m == 3:
            size = img1.shape[:2]
            dPoints = np.array(dstPoints, dtype=np.float32)
            transformada = trAffine(img2, dPoints, srcPoints, size)
            finalImage = insertImage(img1, transformada, dPoints.tolist())
            img1 = finalImage
            cv2.imshow('img1', finalImage)
        else:
            if m == 0:
                print('Debe seleccionar 3 puntos en la imagen')
            else:
                print('Necesita seleccionar', 3 - m, 'puntos más')
    elif k == 27:
        break

cv2.destroyAllWindows()
