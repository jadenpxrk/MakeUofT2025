# too slow
import cv2
import numpy as np
import streamlit as st
import time

# Constants and network parameters
image_width = 600
image_height = 600
threshold = 0.2

# Body parts mapping and POSE_PAIRS for potential further use
BODY_PARTS = {
    "Nose": 0,
    "Neck": 1,
    "RShoulder": 2,
    "RElbow": 3,
    "RWrist": 4,
    "LShoulder": 5,
    "LElbow": 6,
    "LWrist": 7,
    "RHip": 8,
    "RKnee": 9,
    "RAnkle": 10,
    "LHip": 11,
    "LKnee": 12,
    "LAnkle": 13,
    "REye": 14,
    "LEye": 15,
    "REar": 16,
    "LEar": 17,
    "Background": 18,
}

POSE_PAIRS = [
    ["Neck", "RShoulder"],
    ["Neck", "LShoulder"],
    ["RShoulder", "RElbow"],
    ["RElbow", "RWrist"],
    ["LShoulder", "LElbow"],
    ["LElbow", "LWrist"],
    ["Neck", "RHip"],
    ["RHip", "RKnee"],
    ["RKnee", "RAnkle"],
    ["Neck", "LHip"],
    ["LHip", "LKnee"],
    ["LKnee", "LAnkle"],
    ["Neck", "Nose"],
    ["Nose", "REye"],
    ["REye", "REar"],
    ["Nose", "LEye"],
    ["LEye", "LEar"],
]

# Load the TensorFlow DNN model (ensure "graph_opt.pb" is in the correct location)
net = cv2.dnn.readNetFromTensorflow("graph_opt.pb")

# Camera stream URL (modify as needed)
STREAM_URL = "http://192.168.4.1:81/stream"


def get_video_capture():
    """
    Returns a persistent VideoCapture object stored in session_state.
    """
    if "cap" not in st.session_state:
        st.session_state.cap = cv2.VideoCapture(STREAM_URL)
    return st.session_state.cap


def get_frame():
    """
    Reads one frame from the camera stream, applies pose estimation,
    and returns the processed frame (in RGB format).
    """
    cap = get_video_capture()
    ret, frame = cap.read()
    if not ret:
        st.error("Failed to retrieve frame from stream.")
        return None

    # Convert frame from BGR to RGB.
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    photo_height, photo_width, _ = frame_rgb.shape

    # Preprocess the frame.
    blob = cv2.dnn.blobFromImage(
        frame_rgb,
        1.0,
        (image_width, image_height),
        (127.5, 127.5, 127.5),
        swapRB=True,
        crop=False,
    )
    net.setInput(blob)
    out = net.forward()
    out = out[:, :19, :, :]
    assert len(BODY_PARTS) == out.shape[1]

    N = 2  # Number of top local maxima to detect per body part

    # Process each body part heatmap.
    for i, part in enumerate(BODY_PARTS):
        heatMap = out[0, i, :, :]
        local_maxes = []
        # Find local maxima (skip border pixels).
        for y in range(1, heatMap.shape[0] - 1):
            for x in range(1, heatMap.shape[1] - 1):
                if (
                    heatMap[y, x] > heatMap[y - 1, x]
                    and heatMap[y, x] > heatMap[y + 1, x]
                    and heatMap[y, x] > heatMap[y, x - 1]
                    and heatMap[y, x] > heatMap[y, x + 1]
                ):
                    local_maxes.append((heatMap[y, x], (x, y)))
        # Select top N candidates.
        local_maxes.sort(reverse=True, key=lambda x: x[0])
        top_local_maxes = local_maxes[:N]

        # For each candidate above the confidence threshold, draw an ellipse.
        for conf, point in top_local_maxes:
            x_coord = (photo_width * point[0]) / out.shape[3]
            y_coord = (photo_height * point[1]) / out.shape[2]
            if conf > threshold:
                cv2.ellipse(
                    frame_rgb,
                    (int(x_coord), int(y_coord)),
                    (3, 3),
                    0,
                    0,
                    360,
                    (255, 0, 0),
                    cv2.FILLED,
                )
    return frame_rgb


def main():
    st.title("Live Camera Stream with Pose Estimation (Looped)")
    st.write("Rendering video stream with live-updating image placeholder.")

    # Setup stop stream flag in session_state.
    if "stop_stream" not in st.session_state:
        st.session_state.stop_stream = False

    # Define stop callback to set the flag.
    def stop_callback():
        st.session_state.stop_stream = True

    # Place the stop button in the sidebar with a unique key.
    st.sidebar.button("Stop Stream", on_click=stop_callback, key="stop_stream_btn")

    image_placeholder = st.empty()

    # Loop until the stop flag is set.
    while not st.session_state.stop_stream:
        frame = get_frame()
        if frame is not None:
            image_placeholder.image(frame, channels="RGB")
        else:
            st.error("No frame available to display.")
        time.sleep(0.1)

    # Cleanup video capture.
    if "cap" in st.session_state:
        st.session_state.cap.release()
        del st.session_state.cap


if __name__ == "__main__":
    main()
