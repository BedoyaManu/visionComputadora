import cv2
import numpy as np

points = []
rack_height = 0.422
rack_width = 0.242

image = cv2.imread('estantes.jpg')

def select_points(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) > 4:
            points.append((x,y))
            cv2.circle(image, (x,y), 3, (0,0,255), -1)
            cv2.imshow('image', image)
        else:
            print("Debe seleccionar solo 4 puntos, intente nuevamente.")
            points = []

def line_intersection(line1, line2):

    def det(a,b):
        return a[0] * b[1] - a[1] * b[0]
    
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(xdiff, ydiff)

    if div == 0:
        raise Exception('Lineas paralelas')
    
    d = (det(line1[0], line1[1]), det(line2[0], line2[1]))

    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return x, y

cv2.imshow('image', image)
cv2.setMouseCallback('image', select_points)

while True:
    k = cv2.waitKey(1) & 0xFF
    if k == ord('r') and len(points) == 4:
        line1 = [points[0], points[1]]
        line2 = [points[2], points[3]]
        
        vanishing_point = line_intersection(line1, line2)

