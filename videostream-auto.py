import cv2
import numpy as np



BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]


image_width=600
image_height=600


net = cv2.dnn.readNetFromTensorflow("graph_opt.pb")

threshold=0.2


def main():
    stream_url = "http://192.168.4.1:81/stream"
    #esp's ip is set to this. Its port is always 81 for how we coded it.

    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Error: Could not open stream.")
        return


    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to retrieve frame from stream.")
            break
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        photo_height=img.shape[0]
        photo_width=img.shape[1]
        net.setInput(cv2.dnn.blobFromImage(img, 1.0, (image_width, image_height), (127.5, 127.5, 127.5), swapRB=True, crop=False))

        out = net.forward()
        out = out[:, :19, :, :] 

        assert(len(BODY_PARTS) == out.shape[1])

        N = 2
        points = []

        for i in range(len(BODY_PARTS)):
            # Slice heatmap of corresponding body's part.
            heatMap = out[0, i, :, :]

            # Find all local maxima in the heatmap
            local_maxes = []
            for y in range(1, heatMap.shape[0] - 1):
                for x in range(1, heatMap.shape[1] - 1):
                    if (heatMap[y, x] > heatMap[y-1, x] and
                        heatMap[y, x] > heatMap[y+1, x] and
                        heatMap[y, x] > heatMap[y, x-1] and
                        heatMap[y, x] > heatMap[y, x+1]):
                        local_maxes.append((heatMap[y, x], (x, y)))

            # Sort the local maxima by confidence and take the top N
            local_maxes.sort(reverse=True, key=lambda x: x[0])
            top_local_maxes = local_maxes[:N]

            # Append the top N local maxes if their confidence is above the threshold
            for conf, point in top_local_maxes:
                x = (photo_width * point[0]) / out.shape[3]
                y = (photo_height * point[1]) / out.shape[2]
                if conf > threshold:
                    print(conf)
                    points.append((int(x), int(y)))
                    cv2.ellipse(img, points[len(points)-1], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                else:
                    points.append(None)
        t, _ = net.getPerfProfile()
        cv2.imshow("MJPEG Stream with Pose", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break





    #     # Use MediaPipe's Pose with default settings.
    # with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    #     while True:
    #         ret, frame = cap.read()
    #         if not ret:
    #             print("Failed to retrieve frame from stream.")
    #             break

    #         # Convert the image from BGR to RGB as required by MediaPipe.
    #         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         # Process the frame to detect pose.
    #         results = pose.process(frame_rgb)

    #         # If pose landmarks are detected, draw them on the frame.
    #         if results.pose_landmarks:
    #             mp_drawing.draw_landmarks(
    #                 frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
    #                 mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
    #                 mp_drawing.DrawingSpec(color=(0,0,255), thickness=2)
    #             )

    #         # Display the output.
    #         cv2.imshow("MJPEG Stream with Pose", frame)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
