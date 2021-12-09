import cv2
import numpy as np

height = 400
width = 400
image = np.zeros((width, height, 3), dtype=np.uint8)

cv2.imshow('image', image)
for line in range(height * 2):
    image.fill(0)
    cv2.line(image, (0, line//2), (width, line//2),
             (36, 255, 12), thickness=2, lineType=8)
    cv2.imshow('image', image)
    cv2.waitKey(1)

for line in range(height * 2)[::-1]:
    image.fill(0)
    cv2.line(image, (0, line//2), (width, line//2),
             (36, 255, 12), thickness=2, lineType=8)
    cv2.imshow('image', image)
    cv2.waitKey(1)
