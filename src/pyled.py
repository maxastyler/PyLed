#!/usr/bin/env python3

#Colours are a vector with range 0->1
from time import sleep, time

def clamp(minimum, value, maximum):
    if value<minimum: return minimum
    elif value > maximum: return maximum
    else: return value

class Light:
    def __init__(self, RGB=[0, 0, 0], brightness=1):
        self.col=[clamp(0, i, 1) for i in RGB]
        self.bright=clamp(0, brightness, 1)

    def to_duty(self):
        return (self.col[0]*self.bright, self.col[1]*self.bright, self.col[2]*self.bright)

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
        self.cur_time = time

    def tick(self, delta_t):
        self.cur_time -= delta_t
        if self.cur_time < 0:
            self.cur_time = 0

    def fraction(self):
        return 1-self.cur_time/self.time

class PyLed:
    def __init__(self, pin_r, pin_g, pin_b, RGB=[0, 0, 0]):

if __name__=='__main__':
    a=Light([1, 1, 1], 0)
    b=TimeLight(Light([1, 1, 1], 1), 10)
    time_now = time()
    time_end=time()
    while time()-time_now < 10:
        time_start=time_end
        frac=b.fraction()
        print((a*(1-frac)+ b.light*frac).to_duty())
        time_end=time()
        b.tick(time_end-time_start)
