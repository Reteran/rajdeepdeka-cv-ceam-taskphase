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
