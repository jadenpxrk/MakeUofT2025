import cv2 as cv
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


net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

threshold=0.2

img = cv.imread('./dnn_two_test.png',cv.IMREAD_UNCHANGED)
if img.shape[-1] == 4:  # If the image has 4 channels (RGBA)
    img = cv.cvtColor(img, cv.COLOR_RGBA2BGR)

photo_height=img.shape[0]
photo_width=img.shape[1]
net.setInput(cv.dnn.blobFromImage(img, 1.0, (image_width, image_height), (127.5, 127.5, 127.5), swapRB=True, crop=False))

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
            cv.ellipse(img, points[len(points)-1], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
        else:
            points.append(None)
# points = []
# for i in range(len(BODY_PARTS)):
#         # Slice heatmap of corresponging body's part.
#     heatMap = out[0, i, :, :]

#         # Originally, we try to find all the local maximums. To simplify a sample
#         # we just find a global one. However only a single pose at the same time
#         # could be detected this way.
#     for j in range(N):
#         _, conf, _, point = cv.minMaxLoc(heatMap)
#         x = (photo_width * point[0]) / out.shape[3]
#         y = (photo_height * point[1]) / out.shape[2]
#         # Add a point if it's confidence is higher than threshold.
#         points.append((int(x), int(y)) if conf > threshold else None)


# for pair in POSE_PAIRS:
#     partFrom = pair[0]
#     partTo = pair[1]
#     assert(partFrom in BODY_PARTS)
#     assert(partTo in BODY_PARTS)

#     idFrom = BODY_PARTS[partFrom]
#     idTo = BODY_PARTS[partTo]

#     if points[idFrom] and points[idTo]:
#         cv.line(img, points[idFrom], points[idTo], (0, 255, 0), 3)
#         cv.ellipse(img, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
#         cv.ellipse(img, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

t, _ = net.getPerfProfile()

cv.imshow("cool",img)
  
#waits for user to press any key 
#(this is necessary to avoid Python kernel form crashing)
cv.waitKey(0) 
  
#closing all open windows 
cv.destroyAllWindows() 