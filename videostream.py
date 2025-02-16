import cv2
import requests
import numpy as np

# URL of the ESP32 camera stream
stream_url = "http://<ESP32_IP_ADDRESS>/stream"

# Open the stream
stream = requests.get(stream_url, stream=True)

# Initialize OpenCV for displaying the stream
bytes_data = bytes()
for chunk in stream.iter_content(chunk_size=1024):
    bytes_data += chunk
    a = bytes_data.find(b'\xff\xd8')  # Start of JPEG frame
    b = bytes_data.find(b'\xff\xd9')  # End of JPEG frame
    if a != -1 and b != -1:
        jpg = bytes_data[a:b+2]  # Extract the JPEG frame
        bytes_data = bytes_data[b+2:]  # Remove the processed frame from the buffer
        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow('ESP32 Camera Stream', frame)
        if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
            break

cv2.destroyAllWindows()