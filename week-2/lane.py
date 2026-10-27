import cv2 as cv
import numpy as np

filename = "hill.jpg"
road = cv.imread(f'pictures/{filename}')
cv.imshow("road", road)

gblur = cv.GaussianBlur(road, (5,5), 0)
cv.imshow("blur", gblur)

hsv_road = cv.cvtColor(gblur, cv.COLOR_BGR2HSV)
h,s,v = cv.split(hsv_road)

blank = np.zeros(road.shape[:2], dtype = 'uint8')

white = cv.inRange(hsv_road, np.array([0, 0, 170]),  np.array([179, 60, 255]))
yellow = cv.inRange(hsv_road, np.array([10, 60, 80]), np.array([35, 255, 255]))
union = cv.bitwise_or(white,yellow)
cv.imshow('yellow', yellow)
cv.imshow('white', white)
cv.imshow('both', union)

color_mask = cv.bitwise_and(hsv_road, hsv_road, mask=union)
cv.imshow('color mask', color_mask)

# claude
h,w = color_mask.shape[:2]

polygon = np.array([[
    (0, h),
    (w, h),
    (int(0.65 * w), int(0.40 * h)),
    (int(0.40 * w), int(0.40 * h)),
]], dtype=np.int32)

roi_mask = np.zeros_like(color_mask)
cv.fillPoly(roi_mask, polygon, 255)
#claude

roi_img = cv.bitwise_and(roi_mask, color_mask)
cv.imshow('with roi',roi_img)

canny = cv.Canny(union, 50, 150)
cv.imshow("canny", canny)

cv.waitKey(0)


# resources
#
# https://www.slideshare.net/slideshow/lane-detection/125673485