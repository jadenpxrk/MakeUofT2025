import cv2
cap_front = cv2.VideoCapture(1) #front
cap_back = cv2.VideoCapture(1) #back
active_capture = cap_front
while True:
    ret, frame = active_capture.read()

    key = cv2.waitKey(1)
    if key == ord("b"):
        active_capture = cap_back
    elif key == ord("f"):
        active_capture = cap_front
        cv2.imshow(" ",frame)
    if key == ord('q'):
        break