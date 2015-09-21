#!/usr/bin/env python
import time
from abc import ABCMeta, abstractmethod
import argparse
import time
import pygame

from multiprocessing import Process, Queue

from pygame.locals import *


import numpy as np
import os
#PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = "/home/pi/"

try:
    import pigpio
except RuntimeError:
    print("Error importing RPi.RPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

class Stepper(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        #self.__step = 0
	self._pi = pigpio.pi()

    def release(self):
        print("RPIO cleanup")
        #RPIO.cleanup()		
        print("...done...")

class SoncebosStepper(Stepper):

    def __init__(self):
        Stepper.__init__(self)
        self.__name = "8660R013"
        self.__version = 1.0
        #self.__dir = 1.0        # direction ( 0 | cw ) vs ( 1 | ccw )
        #self.__enable = 0.0     # power on 0/1 <--> off/on respectively        

        self.directionPin = 23 #cw/ccw - the directional pin (False=cw)
        self.startPin = 24 #move yes/no pwm
        self.enablePin = 22 #enable engine yes/no
        self.detectPinTop = 17
        self.detectPinBottom = 27

	# replace with self.reset() ?
        self._pi.set_mode(self.directionPin, pigpio.OUTPUT)
        self._pi.set_mode(self.startPin, pigpio.OUTPUT)
        self._pi.set_mode(self.enablePin, pigpio.OUTPUT)
	self._pi.set_mode(self.detectPinTop, pigpio.INPUT)
	self._pi.set_mode(self.detectPinBottom, pigpio.INPUT)	


	self.reset()

        #RPIO.setup(self.detectPinTop, RPIO.IN)
        #RPIO.setup(self.detectPinBottom, RPIO.IN)

        self.secondsToMove =  0.1
        #self.secondsToMove =  0.086956522
        self.frequency_slow = 5000 #5000Hz @ 20s = 2,3cm
	print(self._pi.get_PWM_frequency(self.startPin))


    def reset(self):
        self._pi.write(self.directionPin, 0)
        self._pi.write(self.startPin, 0)
        self._pi.write(self.enablePin, 0)
        self._pi.write(self.detectPinTop, 0)
        self._pi.write(self.detectPinBottom, 0)

    def __str__(self):
        return self.__name + " version " + str(self.__version)

    def upOneStep(self):
	top_is_hit = bool(int(self._pi.read(self.detectPinTop)))
	self._pi.set_pull_up_down(self.detectPinTop, pigpio.PUD_DOWN)
	#print(" top_is_hit ? : " + str(top_is_hit))
        if not top_is_hit:
    	    #print("moving up")
            self._pi.write(self.directionPin, 1)
            self._pi.write(self.enablePin, 0)
            #pwm = RPIO.PWM(self.startPin, self.frequency_slow) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
            #pwm.start(50) #number is percentage of duty cycle: 1-50 works without problems or differences
	    self._pi.set_PWM_frequency(self.startPin,self.frequency_slow)
	    #print("setted frequency :" + str(self._pi.get_PWM_frequency(self.startPin)))
	    self._pi.set_PWM_dutycycle(self.startPin, 128) # PWM 1/2 on
            time.sleep(self.secondsToMove) #number is seconds to go up
	    self._pi.set_PWM_dutycycle(self.startPin, 0) # PWM 1/2 on -> reset
	    self.reset()
            self._pi.write(self.enablePin, 1)

    def downOneStep(self):
	down_is_hit = bool(int(self._pi.read(self.detectPinBottom)))
	self._pi.set_pull_up_down(self.detectPinBottom, pigpio.PUD_DOWN)
	#print(" down_is_hit ? : " + str(down_is_hit))
        if not down_is_hit:
	    #print("moving down")
            self._pi.write(self.directionPin, 0)
            self._pi.write(self.enablePin, 0)
            #pwm = RPIO.PWM(self.startPin, self.frequency_slow) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
            #pwm.start(50) #number is percentage of duty cycle: 1-50 works without problems or differences
	    self._pi.set_PWM_frequency(self.startPin,self.frequency_slow)
	    self._pi.set_PWM_dutycycle(self.startPin, 128) # PWM 1/2 on
            time.sleep(self.secondsToMove) #number is seconds to go up 
	    self._pi.set_PWM_dutycycle(self.startPin, 0) # PWM 1/2 on -> reset
	    self.reset()
            #self._pi.set_pull_up_down(self.enablePin, pigpio.PUD_UP)
            self._pi.write(self.enablePin, 1)

def step_up(stepper):
    for i in range (600):
        stepper.upOneStep()


def step_down(stepper):
    for i in range(600):
        stepper.downOneStep



def pygame_start():

    scale = 0.8
    main_surface = pygame.display.set_mode((int(1920*scale), int(1080*scale)))

    display_black(main_surface)

    return main_surface


def display_black(surface):
    black = (0,0,0)
    surface.fill(black)
    pygame.display.update()

def display_png(surface, path):
    black = (0,0,0)
    surface.fill(black)
    print("clear screen")
    picture = pygame.image.load(path)
    surface.blit(picture, (0, 0))
    print("display image")
    pygame.display.update()


def step_and_wait(t,steps, stepper):

    # do step many steps with stepper
    for i in range(steps):
        stepper.upOneStep()

    time.sleep(t)

def step_back(steps, stepper):
    for i in range(steps):
        stepper.downOneStep()


# def proces_first_line(line, screen, stepper, slice):
#
#     [illumtime, steps, wait] = line
#
#     display_png(screen, slice)
#     time.sleep(illumtime)
#     display_black()
#
#     step_and_wait(illumtime,steps,stepper)
#     step_and_wait(illumtime,steps,stepper)
#     step(steps)



def proces_display_line(line, screen, stepper, slice):

    [illumtime, steps, wait, steps_back] = line

    print("processing slice with illumtime,steps, wait, steps_back = " + str(illumtime) + ", " + str(steps) + ", " + str(wait) + ", " + str(steps_back))
	
    illumtime = float(illumtime)
    steps = int(steps)
    wait = float(wait)
    steps_back = int(steps_back)

    display_png(screen, slice)
    time.sleep(illumtime)
    display_black(screen)

    step_and_wait(wait,steps,stepper)
    step_and_wait(wait,steps,stepper)
    step_back(steps_back,stepper)









def main_processing(slice_path, program, steps):

    #FPSCLOCK = pygame.time.Clock()

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    joysticks[0].init()

    if joysticks[0].get_name() == 'USB Gamepad ':
        print  "Recognized controller: USB Gamepad "
    else:
        print "Error: did not recognize controller"

    # parsed program
    program = np.genfromtxt(program)


    screen = pygame_start()
    display_black(screen)
    print("black screen waiting for start after this")
    stepper = SoncebosStepper()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == JOYBUTTONDOWN:
                if str(event).split()[4][0] == "9":

                    #step_down()

                    for i in range(len(program)):
                       proces_display_line(program[i], screen, stepper, slice_path)

                    # step to top
                    step_up(stepper)
                    display_black(screen)








#parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('slice', metavar='steps',help='The number of steps')
#parser.add_argument('program', metavar='steps',help='The number of steps')
#parser.add_argument('steps', metavar='steps',help='The number of steps')


#results = parser.parse_args()

#print("results " + str(results))

#program_path = PROJECT_PATH + results.program
#steps = int(results.steps)
#slice_path = PROJECT_PATH + results.slice

program_path = PROJECT_PATH + "programm.dat"
slice_path = PROJECT_PATH + "white.png"
steps = 5

main_processing(slice_path,program_path,steps)



