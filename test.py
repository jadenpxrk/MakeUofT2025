import cv2
import streamlit as st
import numpy as np
import requests
import json

# Dummy web server URL (replace with actual endpoint)
SERVER_URL = "https://192.168.1.4:80/posts"

# Load OpenCV pre-trained MobileNet SSD model for object detection
prototxt = cv2.dnn.readNetFromCaffe(cv2.data.haarcascades + "deploy.prototxt", 
                                    cv2.data.haarcascades + "mobilenet_iter_73000.caffemodel")

# Streamlit UI
st.title("Object Detection & Bounding Box JSON Upload")

# Select camera or MJPEG stream
stream_source = st.radio("Select Stream Source", ("Webcam", "MJPEG Stream"))

if stream_source == "MJPEG Stream":
    stream_url = st.text_input("Enter MJPEG Stream URL", "http://192.168.1.4:81/stream")

frame_container = st.empty()

cap = cv2.VideoCapture(0 if stream_source == "Webcam" else stream_url)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.error("Failed to grab frame")
        break

    # Convert BGR to RGB for display
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert frame to blob for DNN
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    prototxt.setInput(blob)
    detections = prototxt.forward()

    bounding_boxes = []

    # Loop through detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:  # Confidence threshold
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], 
                                                        frame.shape[1], frame.shape[0]])
            (x1, y1, x2, y2) = box.astype("int")
            bounding_boxes.append({"x1": x1, "y1": y1, "x2": x2, "y2": y2, "confidence": float(confidence)})

            # Draw bounding box on frame
            cv2.rectangle(rgb_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display frame with bounding boxes
    frame_container.image(rgb_frame, channels="RGB", use_column_width=True)

    # Send JSON data to the dummy web server
    if st.button("Upload JSON"):
        json_data = json.dumps({"bounding_boxes": bounding_boxes})
        response = requests.post(SERVER_URL, json=json_data)
        
        if response.status_code == 201:
            st.success("Bounding boxes uploaded successfully!")
        else:
            st.error("Failed to upload data")

    if st.button("Stop Stream"):
        break

cap.release()
st.write("Stream stopped")
