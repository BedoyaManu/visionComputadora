import cv2
import numpy as np
import math

# Variables
points = []
mPoints = []
shelves_height = 2.1        # Metros reales
shelves_width = 1.1         # Metros reales
original_image = cv2.imread('estantes.jpg')
image = original_image.copy()
warped_image = None
warped_copy = None
selecting_points = True     # Flag para la medición de distancias
oneTimeFlag = True          # Flag para elegir el tamaño de la estantería solo una vez

# Función para elegir las esquinas de la estantería
def click_event(event, x, y, flags, params):
    global points, image, warped_image, warped_copy, oneTimeFlag

    if event == cv2.EVENT_LBUTTONDOWN and oneTimeFlag:
        points.append((x, y))
        cv2.circle(image, (x, y), 3, (0, 0, 255), -1) 
        cv2.imshow('image', image)

        if len(points) == 4:
            pts_src = np.array(points, dtype='float32')
            h, w = int(300 * shelves_height), int(300 * shelves_width)
            pts_dst = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype='float32')
            H = cv2.getPerspectiveTransform(pts_src, pts_dst)
            warped_image = cv2.warpPerspective(original_image, H, (w, h))
            warped_copy = warped_image.copy()
            cv2.imshow('Warped Image', warped_image)
            cv2.setMouseCallback('Warped Image', measure_distance)
            points = []
            print("\nSeleccione dos puntos para medir la distancia entre ellos.")
            oneTimeFlag = False

# Función que mide la distancia entre dos puntos de la imagen
def measure_distance(event, x, y, flags, param):
    global mPoints, warped_copy, selecting_points

    if event == cv2.EVENT_LBUTTONDOWN and selecting_points:
        mPoints.append((x, y))
        cv2.circle(warped_copy, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow('Warped Image', warped_copy)

        if len(mPoints) == 2:
            x0, y0 = mPoints[0]
            x1, y1 = mPoints[1]
            dist = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            print(f"La distancia entre esos dos puntos es de {dist / 300:.2f} m")
            print("Presione 'r' para seleccionar dos puntos más o 'Esc' para salir.")
            selecting_points = False

cv2.imshow('image', image)
cv2.setMouseCallback('image', click_event)

print("Seleccione las 4 esquinas de la estantería.")

while True:
    k = cv2.waitKey(1) & 0xFF
    if k == ord('r') and oneTimeFlag == False:  
        warped_copy = warped_image.copy()
        cv2.imshow('Warped Image', warped_copy)
        print("Seleccione 2 nuevos puntos.")
        mPoints = []
        selecting_points = True
    elif k == 27:
        break

cv2.destroyAllWindows()
