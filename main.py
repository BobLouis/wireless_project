import numpy as np
import cv2
import random
import time
from math import log

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
call_time_glob = 100
# first Minium(Threshold)
al1_time = 0
al1_threshold = 20

# Best_effort choose the closest
al2_time = 0

# Entropy
al3_time = 0
al3_threshold = 25
# self design
al4_time = 0

call_people = 0


def distance(a, b):
    x1 = a[0]
    y1 = a[1]
    x2 = b[0]
    y2 = b[1]
    return ((((x2 - x1)**2) + ((y2-y1)**2))**0.5)


def path_loss(a, b, f):
    # f in Mhz
    x1 = a[0]
    y1 = a[1]
    x2 = b[0]
    y2 = b[1]
    dis = ((((x2 - x1)**2) + ((y2-y1)**2))**0.5)*0.01
    return 87.55 - 20*log(f, 10) - 20*log(dis, 10)


def average(lst):
    return sum(lst) / len(lst)


class Car:
    def __init__(self, id, etr):
        self.id = id
        self.alive = True
        self.call = False
        self.call_start = 0
        self.call_time = 0
        self.al1_connected_base = -1
        self.al2_connected_base = -1
        self.al3_connected_base = -1
        self.al4_connected_base = -1
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
        global car_cnt, call_time_glob, call_people, al1_time, al2_time, al3_time, al4_time, al1_threshold, al3_threshold
        if(self.alive == True):
            if(self.x < 0 or self.y < 0 or self.x > 2500 or self.y > 2500):
                if(self.call == True):
                    call_people -= 1
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
            if(self.call == False and ran < 0.0003):
                self.call = True
                self.call_start = time.time()
                call_people += 1
            if(self.call == True):
                self.call_time = time.time() - self.call_start
                # print(self.call_time)
                sig_list = []  # signal instensity list
                for b in base_list:
                    sig_list.append(
                        round(path_loss((self.x, self.y,), b, base_list.index(b)*100+100), 2))
                # init the base connect to the strongest signal base
                val = max(sig_list)
                strong = sig_list.index(val)  # strongest signal
                avg = average(sig_list)
                if(self.call_time < 0.001):
                    self.al1_connected_base = strong
                    self.al2_connected_base = strong
                    self.al3_connected_base = strong
                    self.al4_connected_base = strong

                # print(sig_list)
                # print('strong', sig_list[strong], 'al1 ', sig_list[self.al1_connected_base], 'al2 ',
                    #   sig_list[self.al2_connected_base], 'al3 ', sig_list[self.al3_connected_base])

                # algo 1 minimum change to the strongest when the signal strength is lower than the threshold
                if(sig_list[self.al1_connected_base] < al1_threshold and self.al1_connected_base != strong):
                    self.al1_connected_base = strong
                    al1_time += 1

                # algo 2 always select the strong
                if(sig_list[self.al2_connected_base] < sig_list[strong]):
                    self.al2_connected_base = strong
                    al2_time += 1

                # algo 3 change to the strong when the original signal is lower than the strongest by 20dB
                if((sig_list[strong] - sig_list[self.al3_connected_base]) > al3_threshold):
                    self.al3_connected_base = strong
                    al3_time += 1

                # algo 4
                if(sig_list[self.al4_connected_base] < avg):
                    self.al4_connected_base = strong
                    al4_time += 1

                # if(closest != self.connected_base):
                #     self.connected_base = closest
                #     print('change')
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
        # cv2.waitKey(1)
        car1.clear_display()


def append_car():
    global duration, car_cnt, start_t, car_id, call_people
    dice = 0.0
    if duration > 0.005:
        car_list.append(Car(car_id, random.randint(0, 35)))
        print("time ", round(time.time()-start_global, 1), "car ", car_id,
              " append ", "car total: ", car_cnt, "call people: ", call_people, "al1: ", al1_time, "al2: ", al2_time, "al3: ", al3_time, "al4: ", al4_time)
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
