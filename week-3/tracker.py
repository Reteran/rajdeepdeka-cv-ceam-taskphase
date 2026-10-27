import cv2 as cv
 
path = "videos/driving-test/driving/o7.mp4"
 
# Open the video file
cap = cv.VideoCapture(path)

# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
else:
    print("Video file opened successfully!")

# Get video properties (e.g., frame count and frame width)
frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))  # Get total number of frames in the video
fps = cap.get(cv.CAP_PROP_FPS)  # Get frames per second (FPS)
print(f"Total frames: {frame_count}, FPS: {fps}")
 
# Read and display each frame of the video
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or error occurred.")
        break

    frame_orb = cv.ORB_create()
    kp = frame_orb.detect(frame, None)
    kp, des = frame_orb.compute(frame, kp)

    frame2 = cv.drawKeypoints(frame, kp, None, color = (0,0,255), flags=0)
    # Display the frame
    cv.imshow("Video Frame", frame2)
 
    # Wait for 1ms for key press to continue or exit if 'q' is pressed
    if cv.waitKey(20) & 0xFF == ord('q'):
        break
 
# Release the video capture object and close any OpenCV windows
cap.release()
cv.destroyAllWindows()

# resources
#
# https://opencv.org/reading-and-writing-videos-using-opencv/