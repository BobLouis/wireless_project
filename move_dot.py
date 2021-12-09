import cv2
import numpy as np

height = 2500  # 1 for 10 m
width = 2500
img = np.zeros((width, height, 3), dtype=np.uint8)
x = 0
y = 250
time = 0
white = (255, 255, 255)
blue = (0, 0, 255)
gree = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
cv2.imshow('img', img)
for i in range(height):
    img.fill(0)
    cv2.rectangle(img, (x+2*i, y-3), (x+2*i+6, y+3), blue, -1)
    cv2.imshow('img', img)
    cv2.waitKey(1)
    cv2.rectangle(img, (x+2*i, y-3), (x+2*i+6, y+3), black, -1)
    time += 1
    print(time)
