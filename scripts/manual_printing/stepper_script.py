#!/usr/bin/env python
import time
from abc import ABCMeta, abstractmethod
import argparse
import time
import pygame
import os

from multiprocessing import Process, Queue
import xml.etree.ElementTree as ET

from pygame.locals import *
import sys


working_mode = "test"
#working_mode = "raspberry_pi"

if working_mode == "raspberry_pi":
    path = "/home/pi/scripts/"
    stepper_enabled = True
    XRES = 1600
    YRES = 900

else:
    path = "/home/mithrawnuruodo/Dev/slaprinter/scripts/"
    stepper_enabled = False
    XRES = 1333
    YRES = 666

import numpy as np
import os
#PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#PROJECT_PATH = "/home/pi/"


#XRES = 1600
#YRES = 900



try:
    if stepper_enabled:
        import pigpio
except RuntimeError:
    print("Error importing RPi.RPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

class Stepper(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        #self.__step = 0
        if stepper_enabled:
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
        if stepper_enabled:
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
        if stepper_enabled:
            print(self._pi.get_PWM_frequency(self.startPin))


    def reset(self):
        if stepper_enabled:
            self._pi.write(self.directionPin, 0)
            self._pi.write(self.startPin, 0)
            self._pi.write(self.enablePin, 0)
            self._pi.write(self.detectPinTop, 0)
            self._pi.write(self.detectPinBottom, 0)
        else:
            print("stepper reset")

    def __str__(self):
        return self.__name + " version " + str(self.__version)

    def upOneStep(self):

        if stepper_enabled:
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
        else:
            print("up one step")

    def downOneStep(self):

        if stepper_enabled:
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
        else:
            print("down one step")

    def step_up(self):
        for i in range (600):
            self.upOneStep()


    def step_down(self):
        for i in range(600):
            self.downOneStep()


main_bus = Queue()


class PygameController(object):

    def __init__(self, stepper, slices, path):
        self.show_eichscreen = False
        self.scale = 1.0
        self.stepper = stepper
        self.screen = None
        self.slice_container = slices
        self.curr_series = 0
        self.path = path
        self.curr_slice = 0
	self.showing_border = False

        #worker_func = lambda: self.check_and_execute_commands()
        #self.processor = Process(target=worker_func)


        # starting functionality
        self.pygame_start()

    @property
    def slices(self):
        return self.slice_container.slices

    def pygame_start(self):
        self.screen = pygame.display.set_mode((int(XRES*self.scale), int(YRES*self.scale)))#, pygame.FULLSCREEN)
        self.display_black()
        #self.processor.start()


    #
    # def restart(self):
    #     '''
    #         use this to cancel current stepper commands by restarting the processor process
    #     :return:
    #     '''
    #
    #     self.processor.join()
    #     main_bus = Queue()
    #     worker_func = lambda: self.check_and_execute_commands()
    #     self.processor = Process(target=worker_func)
    #     self.processor.start()
    #     self.display_black()


    def display_black(self):
        black = (0,0,0)
        self.screen.fill(black)
        pygame.display.update()

    def display_png(self, path):
        black = (0,0,0)
        self.screen.fill(black)
        #print("clear screen")
        picture = pygame.image.load(path)

        img_r = picture.get_rect()

        w = img_r.width
        h = img_r.height


        if w > h:
            r = h/(1.0*w)

            w2 = int(0.9*XRES)
            h2 = int(r*w2)
            picture = pygame.transform.scale(picture, (w2,h2))
        else:

            r = w/(1.0*w)

            h2 = int(0.9*YRES)
            w2 = int(r*h2)
            picture = pygame.transform.scale(picture, (w2,h2))




        x = int((XRES - w2)/2.0)
        y = int((YRES - h2)/2.0)


        self.screen.blit(picture, (x, y))
        print("display image")
        pygame.display.update()


    def step_and_wait(self, wait, steps):

        # do step many steps with stepper
        print("stepping " + str(steps) + " up")
        for i in range(steps):
            self.stepper.upOneStep()
        print("waiting " + str(wait) + " seconds")
        time.sleep(wait)

    def step_back(self, steps):
        print("stepping " + str(steps) + " steps back")
        for i in range(steps):
            self.stepper.downOneStep()



    def proces_display_line(self, line):

        print("line: " + str(line))
        [illumtime, steps, wait, steps_back, stepandwait, slice_id] = line


        #print("processing slice with illumtime,steps, wait, steps_back = " + str(illumtime) + ", " + str(steps) + ", " + str(wait) + ", " + str(steps_back))



        illumtime = float(illumtime)
        steps = int(steps)
        wait = float(wait)
        steps_back = int(steps_back)
        stepandwait = int(stepandwait)
        slice_id = int(slice_id) -1


        slice = self.slices[self.curr_series]



        if slice_id >= len(slice):
            slice_id = len(slice)-1

        print("[slice=" + str(slice_id) + "] path is " + str(slice[slice_id]))

        self.display_png(slice[slice_id])
        time.sleep(illumtime)
        self.display_black()


        for i in range(stepandwait):
            self.step_and_wait(wait,steps)

        self.step_back(steps_back)


    def eich_bild(self):

        if self.show_eichscreen:

            self.display_png(self.path +"eich.png")

        else :

            self.display_black()

        self.show_eichscreen = not self.show_eichscreen



    # def check_and_execute_commands(self):
    #
    #     print("entering check_and_execute_commands")
    #
    #     while True:
    #
    #         while not main_bus.empty():
    #
    #             line = main_bus.get()
    #
    #
    #             type = line[0]
    #             #print("found type : " + str(type))
    #
    #             if type == "main_processing":
    #
    #                 print("main processing")
    #                 if not self.show_eichscreen:
    #                     program = line[1]
    #                     slice_path = line[2]
    #
    #                     self.stepper.step_down()
    #
    #
    #                     #for i in range(len(program)):
    #                     #    self.proces_display_line(program[i], slice_path)
    #
    #                     self.display_black()
    #                     #self.stepper.step_up()
    #
    #
    #             elif type == "display_eich":
    #                 print("display_eich")
    #                 self.eich_bild()
    #
    #             elif type == "step_up":
    #                 print("step_up")
    #                 self.stepper.step_up()
    #
    #             elif type == "step_down":
    #                 print("step_down")
    #                 self.stepper.step_down()
    #
    #             elif type == "down_one_step":
    #                 print("down_one_step")
    #                 self.stepper.downOneStep()
    #
    #             elif type == "up_one_step":
    #                 print("up_one_step")
    #                 self.stepper.upOneStep()
    #
    #
    #
    #


    def display_current(self):

        self.display_black()
        slice = self.slices[self.curr_series]
        #print("current slice is " + str(slice[self.curr_slice]))

        self.display_png(slice[self.curr_slice])
        time.sleep(1)
        self.display_black()



    def display_next_series(self):

        dim = len(self.slices)

        curr = self.curr_series + 1
        if curr >= dim:
            curr = curr % dim



        #print("current slice" + str(curr))
        print("series transision " + str(self.curr_series) + " -> " + str(curr))
        self.curr_series = curr
        self.curr_slice = 0
        self.display_current()


    def next_slice_in_series(self):

        #print("next slice in series")
        dim = len(self.slices[self.curr_series])
        curr = self.curr_slice + 1


        if curr >= dim:
            curr = curr % dim


        self.curr_slice = curr
        self.display_current()




    def show_border(self, pixel):

        self.showing_border = not self.showing_border
        self.display_black()

        if self.showing_border:

            red=(255,0,0)
            pygame.draw.rect(self.screen,red,(0,0,XRES,YRES), pixel)
            pygame.display.update()




    def main_processing(self, program):

        #FPSCLOCK = pygame.time.Clock()

        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        print(joysticks)
        joysticks[0].init()

        if joysticks[0].get_name() == 'USB Gamepad ':
            print  "Recognized controller: USB Gamepad "
        else:
            print "Error: did not recognize controller"

        # parsed program
        program = np.genfromtxt(program)



        self.display_black()
        print("black screen waiting for start after this")
        stepper = SoncebosStepper()

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == JOYBUTTONDOWN:

                    # start button
                    if str(event).split()[4][0] == "9":
                        for i in range(len(program)):
                            self.proces_display_line(program[i])

                        print(">> ... printing executed ... <<")
                        
                    # select button
                    if event.button == 8:
                        self.eich_bild()
                    # x buton
                    if event.button == 0:
                        self.show_border(4)
                    # y button
                    if event.button == 3:
                        self.display_current()
                    # a button
                    if event.button == 1:
                        self.display_next_series()
                    # b button
                    if event.button == 2:
                        self.next_slice_in_series()
                    # left shoulder
                    if event.button == 4:
                        #main_bus.put("step_up")
                        self.stepper.step_up()
                    # right shoulder
                    if event.button == 5:
                        #main_bus.put(["step_down"])
                        print("stepping to downwards end")
                        self.stepper.step_down()

                elif event.type == JOYAXISMOTION:
                    # down pressed
                    if event.joy == 0 and event.axis == 1 and event.value > 0.5:
                        #main_bus.put(["down_one_step"])
                        for i in range(1):
                            self.stepper.downOneStep()

                    # up pressed
                    if event.joy == 0 and event.axis == 1 and event.value < -0.5:
                        #main_bus.put(["up_one_step"])
                        for i in range(1):
                            self.stepper.upOneStep()

                    # right pressed
                    if event.joy == 0 and event.axis == 0 and event.value > 0.5:
                        for i in range(5):
                            #main_bus.put(["up_one_step"])
                            self.stepper.upOneStep()
                    # left pressed
                    if event.joy == 0 and event.axis == 0 and event.value < -0.5:
                        for i in range(5):
                            self.stepper.downOneStep()




class SliceSeriesContainer(object):

    def __init__(self, path):

	self.path = path
        listing = os.listdir(path)

        self.slices = []

        if "slices" in listing:
            self.find_slice_series()


    def find_slice_series(self):


        series_names = [x[0] for x in os.walk(self.path + "slices")]


        ##print("series: " + str(series_names))

        # only take subfolders of slices
        #print("removing: " + str(self.path + "slices"))
        series_names.remove(str(self.path + "slices"))
	


        i = 0

        for series in series_names:
            #print("folder is : " + str(series))


            listing_all = os.listdir(series)
            #print("listing_all : " + str(listing_all))

            listing = [str(series) + "/" + el for el in listing_all if ".png" in el]

            line = {}

            if "conf.xml" in listing_all:
                line = self.parse(str(series) + "/conf.xml", str(series) + "/")
                #print("found listing with config as : ")
                #print(line)

                #print("")
                #print("")
                #print("")
            else:
                n = len(listing)
                for i in range(n):
                    line[i] = listing[i]

                #if n > 1:
                #    print("found listing without config as : ")
                #    print([n,line])

            self.slices.append(line)





    def parse(self,xml, path):
        tree = ET.parse(xml)
        root = tree.getroot()

        dict = {}

        for line in root:

            name = ""
            id = -1

            if line.tag == "line":
                name = line.attrib["name"]
                #print("name: " + str(name))


                for ch in line:
                    if ch.tag == "id":
                        print(ch.text)
                        id = int(ch.text)
                        break

            if name != "" and id >= 0:
                id = id -1
                #print("found name : " + str(name) + " with id = " + str(id))
                dict[id] = path + name


        return dict






#parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('slice', metavar='steps',help='The number of steps')
#parser.add_argument('program', metavar='steps',help='The number of steps')
#parser.add_argument('steps', metavar='steps',help='The number of steps')


#results = parser.parse_args()

#print("results " + str(results))

#program_path = PROJECT_PATH + results.program
#steps = int(results.steps)
#slice_path = PROJECT_PATH + results.slice


#slice_path = "white.png"
#steps = 5



program_path = path + "programm.dat"

slices = SliceSeriesContainer(path=path)

stepper = SoncebosStepper()
controller = PygameController(stepper, slices, path=path)
controller.main_processing(program_path)



