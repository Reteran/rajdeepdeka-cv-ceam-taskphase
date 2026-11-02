# Week 1: Pure Python Image Processor
### What I Implemented:
* A menu system that waits for input from the user and performs some image processing function according to the input
* A brightness increasing/decreasing function
* A function that thresholds the image after asking the user to input the threshold value
* An image rotation function and a flipper function
* An image inverting function
* An image blurring function, which asks the user for an odd numbered kernel size (n) and populates every element of the kernel with 1/n*n
* An Edge detector function that uses the horizontal change detector (Gx) of the sobel filter


Gx = 

     [ -1, 0, 1]
     [ -2, 0, 2]
     [ -1, 0, 1]

* A PGM P2 filereader and writer, used in every function, for tangible outputs
<img width="574" height="347" alt="image" src="https://github.com/user-attachments/assets/1feff581-5d14-41d9-b1d1-eae09bba0139" />

### Challenges

The most challenging part was implementing the neighborhood operations, especially the padding function required for them, which took a lot of trial and error and changing of different parameters before I could get it to work. 

An unexpected challenge was implementing the PGM filereader/writer. I had to make the code work its way through the formatting of the file and extract information from it like the height, width and max pixel intensity and get a hang of whitespace handling string functions in python.

<img width="639" height="484" alt="image" src="https://github.com/user-attachments/assets/8fd5b1c4-92ec-489e-9b9d-40792264d51d" />  

Original image

<img width="639" height="484" alt="image" src="https://github.com/user-attachments/assets/f81f6660-e528-4346-bc42-7b60e258cd68" />  

Edge Detection

<img width="640" height="477" alt="image" src="https://github.com/user-attachments/assets/a02d2ec3-97c6-4a67-96c6-efac6f076311" />  

Thresholded image


# Week 2: Lane Line Separator
# Week 3: Classical Tracking and Feature Detection
### What I Implemented:
* An ORB feature detector (1500 features) that finds keypoints and 256-bit binary descriptors in every frame of a driving video
* A frame-to-frame feature matcher that compares descriptors of consecutive frames using Hamming distance (brute force, k = 2 nearest neighbours)
* Lowe's ratio test, which keeps a match only if the best match is clearly better than the second best (distance < 0.7 × second best distance)
* RANSAC verification using a homography, which splits the remaining matches into inliers and outliers using a 3 px reprojection threshold
* A warped outline of the previous frame drawn on the current frame using the homography (perspectiveTransform + polylines), which shows the overall camera motion between frames
* A Lucas-Kanade sparse optical flow tracker that picks Shi-Tomasi corners in the first frame and tracks them through the video with pyramidal LK, drawing a coloured track for each point

Pipeline for the matcher:

    frame N-1, frame N -> grayscale -> ORB keypoints + descriptors
                       -> knnMatch (Hamming, k=2) -> Lowe's ratio test
                       -> findHomography (RANSAC) -> inliers






ORB matches (inliers only) with the warped frame outline

Lucas-Kanade optical flow tracks

### Vehicle Motion Tracker
*Status: in progress.* Vehicle detection and per-vehicle tracking is not finished yet. The plan is to detect vehicles, find corners inside each bounding box, track them with Lucas-Kanade, and move each box by the median displacement of its tracked points, recording the displacement in pixels per frame.

### Challenges

The hardest part was understanding what the data structures returned by OpenCV actually mean, especially the match objects (queryIdx refers to the previous frame's keypoints, trainIdx to the current frame's) and the (N, 1, 2) point arrays that functions like findHomography and perspectiveTransform expect. Getting the order of src and dst wrong does not raise an error, it just gives a garbage homography.

Several bugs only appeared on particular frames:
* `knnMatch` with k=2 crashed when the matcher was created with `crossCheck=True`, because cross-checking only works with k=1.
* When the camera moved fast, the blurred frames produced few matches, so the `inliers` list from an earlier frame was reused and its indices pointed outside the current keypoint list, crashing `drawMatches`. Resetting the per-frame variables at the start of every iteration fixed it.
* Passing `matchesMask` to `drawMatches` together with an already filtered match list gave a size mismatch error, so I filter the list instead.

Another challenge was seeing why the feature matching on its own is not vehicle tracking. The homography only describes how the whole scene moves between frames, and nothing in it knows what a vehicle is, so a separate detection and tracking step is still needed.
