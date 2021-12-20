import numpy as np
import cv2
import random
import time


height = 2500  # 1 for 10 m
width = 2500
cnt = 0
x = 0
y = 250
# time = 0
white = (255, 255, 255)
blue = (0, 0, 255)
gree = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
car_stk = []
img = np.zeros((width, height, 3), np.uint8)
img.fill(0)
car_cnt = 0
car_id = 0
dir_x = [1, 0, -1, 0]
dir_y = [0, -1, 0, 1]
car_list = []
base_list = []
start_t = time.time()
duration = 0.0


class Car:
    def __init__(self, id, etr):
        self.id = id
        self.alive = True
        global img

        if(int(etr/9) == 0):
            self.x = 0
            self.y = 250*((etr % 9)+1)
            self.dir = 0
        elif(int(etr/9) == 1):
            self.x = 250*((etr % 9)+1)
            self.y = 2500
            self.dir = 1
        elif(int(etr/9) == 2):
            self.x = 2500
            self.y = 250*((etr % 9)+1)
            self.dir = 2
        else:
            self.x = 250*((etr % 9)+1)
            self.y = 0
            self.dir = 3

    def update(self):
        global car_cnt
        if(self.x < 0 or self.y < 0 or self.x > 2500 or self.y > 2500):
            self.alive = False
            car_cnt -= 1

        x_dir = {0: 1, 1: 0, 2: -1, 3: 0}
        y_dir = {0: 0, 1: -1, 2: 0, 3: 1}
        if(self.x > 0 and self.x < 2500 and self.y < 2500 and self.y > 0 and self.x % 250 == 0 and self.y % 250 == 0):
            ran = random.random()
            if ran < 0.5:
                self.x += x_dir[self.dir]
                self.y += y_dir[self.dir]
            elif (ran < 0.71875):
                self.dir -= 1
                if self.dir < 0:
                    self.dir += 4
                self.x += x_dir[self.dir]
                self.y += y_dir[self.dir]
            elif(ran < 0.9375):
                self.dir += 1
                if self.dir > 3:
                    self.dir -= 4
                self.x += x_dir[self.dir]
                self.y += y_dir[self.dir]
            else:
                if(self.dir == 0):
                    self.dir = 2
                elif(self.dir == 1):
                    self.dir = 3
                elif(self.dir == 2):
                    self.dir = 0
                else:
                    self.dir = 1
                self.x += x_dir[self.dir]
                self.y += y_dir[self.dir]
        else:
            self.x += x_dir[self.dir]
            self.y += y_dir[self.dir]

    def display(self):
        global car_list
        if(self.alive):
            cv2.rectangle(img, (self.x-8, self.y-8),
                          (self.x+8, self.y+8), blue, -1)
            # cv2.imshow('img', img)
            # print('id', self.id, '(', self.x, self.y, ') direc', self.dir)
        else:
            car_list.remove(self)
            del self

    def clear_display(self):
        if(self.alive):
            cv2.rectangle(img, (self.x-8, self.y-8),
                          (self.x+8, self.y+8), white, -1)


def create_map():
    # row
    for i in range(9):
        cv2.line(img, (0, 250+250*i), (2500, 250+250*i), (255, 255, 255), 16)
    # col
    for i in range(9):
        cv2.line(img, (250+250*i, 0), (250+250*i, 2500), (255, 255, 255), 16)
    # 顯示圖片
    cv2.imshow('img', img)


def create_base():
    global img

    for i in range(10):
        for j in range(10):
            ran = random.random()
            if(ran < 0.1):
                if(ran < 0.025):
                    pt1 = (125+250*i+10, 100+250*j)
                    pt2 = (100+250*i+10, 150+250*j)
                    pt3 = (150+250*i+10, 150+250*j)
                    base_list.append((125+250*i+10, 125+250*j))
                elif(ran < 0.05):
                    pt1 = (125+250*i-10, 100+250*j)
                    pt2 = (100+250*i-10, 150+250*j)
                    pt3 = (150+250*i-10, 150+250*j)
                    base_list.append((125+250*i-10, 125+250*j))
                elif(ran < 0.075):
                    pt1 = (125+250*i, 100+250*j+10)
                    pt2 = (100+250*i, 150+250*j+10)
                    pt3 = (150+250*i, 150+250*j+10)
                    base_list.append((125+250*i, 125+250*j+10))
                else:
                    pt1 = (125+250*i, 100+250*j-10)
                    pt2 = (100+250*i, 150+250*j-10)
                    pt3 = (150+250*i, 150+250*j-10)
                    base_list.append((125+250*i, 125+250*j-10))

                triangle_cnt = np.array([pt1, pt2, pt3])
                cv2.drawContours(img, [triangle_cnt], 0, (0, 255, 0), -1)
                cv2.imshow("img", img)


def create_car():
    car1 = Car(1, random.randint(0, 35))
    while True:
        car1.update()
        car1.display()
        cv2.imshow('img', img)
        cv2.waitKey(1)
        car1.clear_display()


def append_car():
    global duration
    global car_cnt
    global start_t
    global car_id
    dice = 0.0
    if duration > 1:
        car_list.append(Car(car_id, random.randint(0, 35)))
        print("car ", car_id, " append")
        car_cnt += 1
        car_id += 1
        duration = 0.0
        start_t = time.time()

    duration = time.time()-start_t


def update_car():
    for car in car_list:
        car.update()
        car.display()
    cv2.imshow('img', img)
    cv2.waitKey(1)
    # sleep(0.01)
    for car in car_list:
        car.clear_display()


create_map()
create_base()
print(base_list)
while(True):
    append_car()
    update_car()
