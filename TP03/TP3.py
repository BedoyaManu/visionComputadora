import sys
import cv2

if(len(sys.argv) > 1):
    filename = sys.argv[1]
else:
    print("Pass a filename as first argument")
    sys.exit(0)

cap = cv2.VideoCapture(filename)

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
fps = cap.get(cv2.CAP_PROP_FPS)
width = cap.get(3)
height = cap.get(4)
framesize = (int(width),int(height))
out = cv2.VideoWriter('output.avi', fourcc, fps, framesize)

delay = int(1000/fps)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret is True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(gray)
        cv2.imshow('Image gray', gray)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()