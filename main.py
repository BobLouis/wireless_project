import numpy as np
import cv2

height = 2500  # 1 for 10 m
width = 2500
x = 0
y = 250
time = 0
white = (255, 255, 255)
blue = (0, 0, 255)
gree = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
img = np.zeros((width, height, 3), np.uint8)


def create_map():
    # row
    for i in range(9):
        cv2.line(img, (0, 250+250*i), (2500, 250+250*i), (255, 255, 255), 3)
    # col
    for i in range(9):
        cv2.line(img, (250+250*i, 0), (250+250*i, 2500), (255, 255, 255), 3)
    # 顯示圖片
    cv2.imshow('img', img)
    for i in range(height):
        cv2.rectangle(img, (x+2*i, y-3), (x+2*i+6, y+3), blue, -1)
        cv2.imshow('img', img)
        cv2.waitKey(1)
        cv2.rectangle(img, (x+2*i, y-3), (x+2*i+6, y+3), white, -1)
    # 按下任意鍵則關閉所有視窗
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def add_dot():
    for i in range(height):
        img.fill(0)
        cv2.rectangle(img, (x+2*i, y-3), (x+2*i+6, y+3), blue, -1)
        cv2.imshow('img', img)
        cv2.waitKey(1)
        time += 1
        print(time)


class Car:
    def __init__(self, id, etr_x, etr_y):
        self.id = id
        self.x = etr_x
        self.y = etr_y

    def print(self):
        print(self.id)
        print(self.x)
        print(self.y)


img.fill(0)
create_map()
add_dot()
