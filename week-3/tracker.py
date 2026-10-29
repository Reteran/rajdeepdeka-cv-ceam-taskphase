import cv2 as cv
import numpy as np
 
path = "videos/driving-test/driving/o9.mp4"

cap = cv.VideoCapture(path)

if not cap.isOpened():
    print("Error: Could not open video file.")
else:
    print("Video file opened successfully.")

# Get video properties (e.g., frame count and frame width)
frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))  # Get total number of frames in the video
fps = cap.get(cv.CAP_PROP_FPS)  # Get frames per second (FPS)
print(f"Total frames: {frame_count}, FPS: {fps}")

prev = None
prev_keys = None
prev_des = None
prev_gray = None

orb = cv.ORB_create()
bf = cv.BFMatcher(cv.NORM_HAMMING)

MIN_MATCH_COUNT = 10

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or error occurred.")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    keys, des = orb.detectAndCompute(gray, None)

    if prev is not None and prev_keys is not None and prev_des is not None:
        matches = bf.knnMatch(prev_des, des, k=2)
        good = []

        for m in matches:
            if len(m) == 2 and m[0].distance < 0.7 * m[1].distance:
                good.append(m[0])

        if len(good) > MIN_MATCH_COUNT: # if there are enough matches...
            src = np.float32([prev_keys[m.queryIdx].pt for m in good]).reshape(-1,1,2)
            dst = np.float32([keys[m.trainIdx].pt for m in good]).reshape(-1,1,2)

            M, mask = cv.findHomography(src, dst, cv.RANSAC, 3.0)
            if mask is not None:
                good =[m for m, keep in zip(good, mask.ravel()) if keep]

            # frame = cv.polylines(frame, [np.int32(dst)], True, 255, 3, cv.LINE_AA)

        match_frame = cv.drawMatches(prev, prev_keys, frame, keys, good, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)



        cv.imshow("feature matching", match_frame)

    # frame2 = cv.drawKeypoints(frame, keypoints, None, color = (0,0,255), flags=0)
    # cv.imshow("Video Frame", frame2)

    prev = frame
    prev_keys = keys
    prev_des = des
    prev_gray = gray

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
 
# Release the video capture object and close any OpenCV windows
cap.release()
cv.destroyAllWindows()

# resources
#
# https://opencv.org/reading-and-writing-videos-using-opencv/
# https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html
# https://www.geeksforgeeks.org/python/feature-matching-using-orb-algorithm-in-python-opencv/
# https://docs.opencv.org/3.4.20/d1/de0/tutorial_py_feature_homography.html
# https://docs.opencv.org/3.4.20/d5/d6f/tutorial_feature_flann_matcher.html