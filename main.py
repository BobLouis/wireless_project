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
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
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
start_global = start_t
duration = 0.0

# four algorithm
call_time_glob = 30
# first Minium(Threshold)
mini_time = 0
mini_threshold = 80

# Best_effort choose the closest
Best_effort_time = 0

# Entropy
Entropy_time = 0

call_people = 0


def distance(a, b):
    x1 = a[0]
    y1 = a[1]
    x2 = b[0]
    y2 = b[1]
    return ((((x2 - x1)**2) + ((y2-y1)**2))**0.5)


class Car:
    def __init__(self, id, etr):
        self.id = id
        self.alive = True
        self.call = False
        self.call_start = 0
        self.call_time = 0
        self.connected_base = 0
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
        global car_cnt, call_time_glob, call_people
        if(self.alive == True):
            if(self.x < 0 or self.y < 0 or self.x > 2500 or self.y > 2500):
                self.alive = False
                car_cnt -= 1

        x_dir = {0: 1, 1: 0, 2: -1, 3: 0}
        y_dir = {0: 0, 1: -1, 2: 0, 3: 1}
        ran = random.random()
        if(self.x > 0 and self.x < 2500 and self.y < 2500 and self.y > 0 and self.x % 250 == 0 and self.y % 250 == 0):

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
        # calling process
        if(ran < 0.0005 and self.call == False):
            self.call = True
            self.call_start = time.time()
            call_people += 1
        if(self.call == True):
            self.call_time = time.time() - self.call_start
            dis_list = []
            for b in base_list:
                dis_list.append(round(distance((self.x, self.y), b), 2))
            val = min(dis_list)
            closest = dis_list.index(val)
            if(closest != self.connected_base):
                self.connected_base = closest
                print('change')
            if(self.call_time > call_time_glob):
                self.call = False
                self.call_time = 0
                call_people -= 1

    def display(self):
        global car_list
        if(self.alive):
            if(self.call == True):
                cv2.rectangle(img, (self.x-8, self.y-8),
                              (self.x+8, self.y+8), blue, -1)
            else:
                cv2.rectangle(img, (self.x-8, self.y-8),
                              (self.x+8, self.y+8), red, -1)
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
    global duration, car_cnt, start_t, car_id, call_people
    dice = 0.0
    if duration > 0.12:
        car_list.append(Car(car_id, random.randint(0, 35)))
        print("time ", round(time.time()-start_global, 1), "car ", car_id,
              " append ", "car total: ", car_cnt, "call people: ", call_people)
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
