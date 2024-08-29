import cv2
import numpy as np

# URL de la Cámara IP
url = 'http://192.168.0.41:4747/video'
cap = cv2.VideoCapture(url)

# Videos
overlay_mundial = cv2.VideoCapture('copa_mundial.mp4')
overlay_america = cv2.VideoCapture('copa_america.mp4')

# Diccionario
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()

marker_length = 0.1

# Calibración de cámara
camera_matrix = np.array([[1000, 0, 640],
                          [0, 1000, 360],
                          [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.zeros((5, 1))


while True:
    ret, frame = cap.read()
    if not ret:
        print("Cámara no encontrada")
        break

    # Escala de grises del video por IP
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Marcadores detectados
    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Detectamos los marcadores 23 y 33
    if ids is not None:
        # Estimamos la pose de cada marcador
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, camera_matrix, dist_coeffs)

        # Iteramos sobre los marcadores detectados
        for i in range(len(ids)):
            marker_id = ids[i][0]  # ID del marcador detectado

            # Vectores de rotación y traslación
            rvec = rvecs[i][0]
            tvec = tvecs[i][0]
            marker_corners = corners[i].reshape((4, 2))

            # Seleccionamos el video correspondiente al marcador
            if marker_id == 23:
                overlay_video = overlay_mundial
            elif marker_id == 33:
                overlay_video = overlay_america
            else:
                overlay_video = None
                continue

            # Leemos el siguiente frame del video a sobreponer
            ret, video_frame = overlay_video.read()
            if not ret:
                overlay_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, video_frame = overlay_video.read()

            # Hacemos la transformación en perspectiva sobre el marcador
            h, w, _ = video_frame.shape

            pts_dst = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)
            pts_src = np.array(marker_corners, dtype=np.float32)
            M = cv2.getPerspectiveTransform(pts_dst, pts_src)

            warped_frame = cv2.warpPerspective(video_frame, M, (frame.shape[1], frame.shape[0]))

            # Colocamos el video correspondiente sobre el video en tiempo real
            mask = np.zeros_like(frame, dtype=np.uint8)
            cv2.fillConvexPoly(mask, np.int32([marker_corners]), (255, 255, 255))

            frame = cv2.bitwise_and(frame, cv2.bitwise_not(mask))
            frame = cv2.add(frame, warped_frame)

    # Mostramos la imágen final
    cv2.imshow('ArUco Marker Tracking', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
overlay_mundial.release()
overlay_america.release()
cv2.destroyAllWindows()