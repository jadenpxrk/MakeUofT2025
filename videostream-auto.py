import cv2

def main():
    stream_url = "http://192.168.4.1:81/stream"
    #esp's ip is set to this. Its port is always 81 for how we coded it.

    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Error: Could not open stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow("ESP32 Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
