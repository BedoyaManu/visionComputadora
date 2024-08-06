import cv2
import numpy as np

ix, iy = -1, -1
fx, fy = -1, -1

recorte = False


def recortar(event, x, y, flags, param):
    global ix, iy, fx, fy, img, recorte
    if event == cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y
        img = cv2.imread('original.jpg')
    elif event == cv2.EVENT_LBUTTONUP:
        cv2.rectangle(img, (ix, iy), (x, y), (255, 0, 0), 0)
        recorte = True
        fx = x
        fy = y


def trEucl(img, center, angle, x, y):
    """
    Performs Euclidean transformation (rotation and translation) on the image.

    Args:
        img (np.ndarray): The input image.
        center (tuple): The center point for rotation (relative to the image).
        angle (float): The rotation angle in degrees.
        x (int): The x-axis translation for the transformed image.
        y (int): The y-axis translation for the transformed image.

    Returns:
        np.ndarray: The transformed image with the same size as the original image.
    """

    # Get the original image size
    rows, cols = img.shape[:2]

    # Get rotation matrix
    R = cv2.getRotationMatrix2D(center, angle, 1)

    # Combine rotation and translation into a single transformation matrix
    T = np.float32([[1, 0, x], [0, 1, y]])
    M = np.dot(T, R)

    # Perform the transformation using warpAffine and ensure the output size is the same as the original
    transformed = cv2.warpAffine(img, M, (cols, rows))

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

            transformed = trEucl(imgRecortada, (x1 - x0, y1 - y0), angle, tx, ty)
            img[y0:y1, x0:x1] = transformed

            cv2.imwrite('transformada.jpg', img)
            break
        else:
            print('Seleccione una parte de la imagen primero')

    elif k == 27:
        break

cv2.destroyAllWindows()
