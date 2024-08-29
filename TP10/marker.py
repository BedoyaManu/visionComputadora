import cv2 as cv
import numpy as np

# Ensure OpenCV is up to date with contrib modules
print(cv.__version__)  # Check the version of OpenCV

# Cargamos el diccionario predefinido
diccionario = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)

# Generamos el marcador
imagen23 = cv.aruco.generateImageMarker(diccionario, 23, 200)
imagen33 = cv.aruco.generateImageMarker(diccionario, 33, 200)

# Guardamos la imagen del marcador
cv.imwrite("marker23.png", imagen23)
cv.imwrite("marker33.png", imagen33)

# Mostramos la imagen en una ventana
cv.imshow("ventana23", imagen23)
cv.imshow("ventana33", imagen33)
cv.waitKey(0)
cv.destroyAllWindows()