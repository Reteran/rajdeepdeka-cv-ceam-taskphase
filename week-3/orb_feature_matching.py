import cv2 as cv
import numpy as np
 
path = "videos/driving-test/driving/08.mp4"

cap = cv.VideoCapture(0)

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

orb = cv.ORB_create(nfeatures=1500)
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
            '''
            Values which pass the Lowe's Ratio test get appended to good
            '''
            if len(m) == 2 and m[0].distance < 0.7 * m[1].distance:
                good.append(m[0])

        matchesMask = None
        if len(good) > MIN_MATCH_COUNT: # if there are enough matches...
            src = np.float32([prev_keys[m.queryIdx].pt for m in good]).reshape(-1,1,2)
            dst = np.float32([keys[m.trainIdx].pt for m in good]).reshape(-1,1,2)

            M, mask = cv.findHomography(src, dst, cv.RANSAC, 3.0)

            if mask is not None and M is not None:
                '''
                This is essentially just a bitmasking for further refining in the good list.
                mask.ravel() turns mask into a 1d array, which has one entry per input match, 
                according to RANSAC. 1 means the match is an inlier and 0 means it is an outlier.
                we are turning the mask into a 1d array and only retaining those values of good
                which correspond to a 1 (inlier) in the mask.
                '''
                inliers = [m for m, keep in zip(good, mask.ravel()) if keep] 
                outliers = [m for m, keep in zip(good, mask.ravel()) if not keep]
            else:
                inliers = []
                outliers = good

            h,w = prev.shape[:2]
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            outline = cv.perspectiveTransform(pts, M)

            vis = frame.copy()
            cv.polylines(vis, [np.int32(outline)], True, (0,0,255), 5)

        draw_params = dict(matchColor = (0,0,255),
                            singlePointColor=None,
                            # matchesMask=matchesMask, this line is only for if we don't filter good using the list comprehension and still want to display using a matchesMask = mask.ravel().tolist()
                            flags = 2)
        match_frame = cv.drawMatches(prev, prev_keys, vis, keys, inliers, None, **draw_params)
        cv.imshow("feature matching", match_frame)

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