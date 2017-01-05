#!/usr/bin/env python3

#Colours are a vector with range 0->1

class Colour:
    def __init__(self, RGB=[0, 0, 0]):
        self.col=RGB

class PyLed:
    def __init__(self, RGB=[0, 0, 0]):
        self.col = Colour(RGB)

if __name__=='__main__':
    a=PyLed()
