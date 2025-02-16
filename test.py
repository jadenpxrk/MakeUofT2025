import cv2

stream_url = "http://192.168.4.1:81/stream"

# Initialize video capture with the default camera (device 1)
cap = cv2.VideoCapture(stream_url)

# Read the first frame to serve as the background reference
ret, first_frame = cap.read()
if not ret:
    print("Error: Unable to read from camera.")
    cap.release()
    exit()

# Convert first frame to grayscale and blur it
first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
first_gray = cv2.GaussianBlur(first_gray, (21, 21), 0)

# Set sensitivity configuration. Increase threshold to lower sensitivity.
sensitivity_threshold = 145  # Increase from 25 to 50 (or adjust as needed)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert current frame to grayscale and blur it
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Compute the absolute difference between the background and current frame
    frame_delta = cv2.absdiff(first_gray, gray)

    # Apply thresholding with the sensitivity threshold
    thresh = cv2.threshold(frame_delta, sensitivity_threshold, 255, cv2.THRESH_BINARY)[
        1
    ]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Identify contours of moving objects
    contours, _ = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Draw bounding boxes for contours that exceed the minimum area
    for contour in contours:
        if cv2.contourArea(contour) < 700:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame with bounding boxes
    cv2.imshow("Camera Stream", frame)

    # Press 'q' to exit the stream
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
