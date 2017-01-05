#!/usr/bin/env python3

#Colours are a vector with range 0->1
from time import sleep, time
import RPi.GPIO as GPIO

def clamp(minimum, value, maximum):
    if value<minimum: return minimum
    elif value > maximum: return maximum
    else: return value

def interpolate(a, b, frac):
    return a*(1-frac)+b*frac

class Light:
    def __init__(self, RGB=[0, 0, 0], brightness=1):
        self.col=[clamp(0, i, 1) for i in RGB]
        self.bright=clamp(0, brightness, 1)

    def to_duty(self):
        return (self.col[0]*self.bright*100, self.col[1]*self.bright*100, self.col[2]*self.bright*100)

    def __str__(self):
        return "({0}, {1})".format(self.col, self.bright)

    def __add__(self, other):
        return Light([self.col[i] + other.col[i] for i in range(3)], self.bright+other.bright)

    def __sub__(self, other):
        return Light([self.col[i] - other.col[i] for i in range(3)], self.bright-other.bright)

    def __mul__(self, other):
        return Light([other*i for i in self.col], other*self.bright)

class TimeLight:
    def __init__(self, light, time):
        self.light = light
        self.time = time
        self.cur_time = time

    def reset(self):
        self.cur_time = self.time

    def tick(self, delta_t):
        self.cur_time -= delta_t
        if self.cur_time < 0: return True
        else: return False

    def fraction(self):
        return 1-self.cur_time/self.time

class PyLed:
    def __init__(self, pin_r, pin_g, pin_b, RGB=[0, 0, 0]):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        pin_nums=[pin_r, pin_g, pin_b]
        GPIO.setup(pin_nums, GPIO.OUT)
        self.pins=[GPIO.PWM(i, 50) for i in pin_nums]
        self.cur_col=Light()
        self.cur_pos=0
        self.targets=[TimeLight(Light([0, 1, 0], 0.5), 10), TimeLight(Light([0, 1,0], 0), 10)]#, TimeLight(Light([0, 0, 1], 1), 2)]
        for i in self.pins: i.start(100)

    def main_loop(self):
        end_time=time()
        while True:
            start_time=end_time
            duty=interpolate(self.cur_col, self.targets[self.cur_pos].light, self.targets[self.cur_pos].fraction()).to_duty()
            for i in range(len(self.pins)):
                self.pins[i].ChangeDutyCycle(duty[i])
            sleep(0.1)
            end_time = time()
            if self.targets[self.cur_pos].tick(end_time-start_time):
                self.targets[self.cur_pos].reset()
                self.cur_col=self.targets[self.cur_pos].light
                self.cur_pos = (self.cur_pos+1)%len(self.targets)
         
        

if __name__=='__main__':
    a=PyLed(36, 38, 40)
    a.main_loop()
