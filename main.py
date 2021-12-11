import numpy as np
import cv2
import random
from time import sleep


height = 2500  # 1 for 10 m
width = 2500
cnt = 0
x = 0
y = 250
time = 0
white = (255, 255, 255)
blue = (0, 0, 255)
gree = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
car_stk = []
img = np.zeros((width, height, 3), np.uint8)
img.fill(0)
car_cnt = 0
dir_x = [1, 0, -1, 0]
dir_y = [0, -1, 0, 1]



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
        if(self.x < 0 or self.y < 0 or self.x > 2500 or self.y > 2500):
            self.alive = False
        x_dir = {0:1, 1:0, 2:-1, 3:0}
        y_dir = {0:0, 1:-1, 2:0, 3:1}
        if(self.x > 0 and self.x < 2500 and self.y <2500 and self.y > 0 and self.x % 250 == 0 and self.y % 250 == 0):
            ran = random.random()
            if ran < 0.5 :
                self.x += x_dir[self.dir]
                self.y += y_dir[self.dir]
            elif (ran < 0.71875):
                self.dir -= 1
                if self.dir < 0 :
                    self.dir += 4
                self.x += x_dir[self.dir]
                self.y += y_dir[self.dir]
            elif(ran < 0.9375):
                self.dir += 1
                if self.dir > 3 :
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
        if(self.alive):
            cv2.rectangle(img, (self.x-3 , self.y-3), (self.x+3, self.y+3), blue, -1)
            cv2.imshow('img', img)
            print('id',self.id,'(',self.x, self.y,') direc', self.dir)
            
    def clear_display(self):
        if(self.alive):
            cv2.rectangle(img, (self.x-3 , self.y-3), (self.x+3, self.y+3), white, -1)

def create_map():
    # row
    for i in range(9):
        cv2.line(img, (0, 250+250*i), (2500, 250+250*i), (255, 255, 255), 6)
    # col
    for i in range(9):
        cv2.line(img, (250+250*i, 0), (250+250*i, 2500), (255, 255, 255), 6)
    # 顯示圖片
    cv2.imshow('img', img)
    # for i in range(height):
    #     cv2.rectangle(img, (x+2*i, y-3), (x+2*i+6, y+3), blue, -1)
    #     cv2.imshow('img', img)
    #     cv2.waitKey(1)
        #  cv2.rectangle(img, (x+2*i, y-3), (x+2*i+6, y+3), white, -1)
    car1 = Car(1,32)
    car2 = Car(2,34)
    car3 = Car(3,35)
    while True:
        car1.update()
        car2.update()
        car3.update()
        car1.display()
        car2.display()
        car3.display()
        cv2.waitKey(1)
        car1.clear_display()
        car2.clear_display()
        car3.clear_display()   
create_map()

    
    