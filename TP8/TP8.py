import cv2
import numpy as np

points = []
image = None
selecting_points = False

def click_event(event, x, y, flags, params):
    global points, image, selecting_points

    if selecting_points and event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(image, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow('image', image)

        if len(points) == 4:
            pts_src = np.array(points, dtype='float32')
            h, w = 300, 400
            pts_dst = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype='float32')
            H = cv2.getPerspectiveTransform(pts_src, pts_dst)
            warped_image = cv2.warpPerspective(original_image, H, (w, h))
            cv2.imshow('Warped Image', warped_image)
            points = []
            selecting_points = False

original_image = cv2.imread('timeSquare.jpg')
image = original_image.copy()

cv2.imshow('image', image)
cv2.setMouseCallback('image', click_event)

print("Presione 'h' para comenzar la selección de 4 puntos o presione 'Esc' para salir.")

while True:
    k = cv2.waitKey(1) & 0xFF
    if k == ord('h'):
        selecting_points = True
        image = original_image.copy()
        cv2.imshow('image', image)
        print("Seleccione 4 puntos con el mouse.")
    elif k == 27:  # Presiona 'Esc' para salir
        break

cv2.destroyAllWindows()