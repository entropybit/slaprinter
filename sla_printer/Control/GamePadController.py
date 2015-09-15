import random, pygame, sys
from pygame.locals import *
from multiprocessing import Process
#from threading import Thread
from MessageHandler import Observable, MessageBus
from Messages import *
from Config import checking_interval, refresh_cycle

import os
import time


DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/Data"

class GamePadControllerProto(object):

    def __init__(self, joystick_name="unknown"):
        self.joystick_name = joystick_name

    def __str__(self):
        return "joystick [" + self.joystick_name + "] found"


class GamePadController(Observable, Process):

    def __init__(self, bus, fps=30):
        Process.__init__(self)
        Observable.__init__(self, bus=bus)

        self.fps = fps # frames per second, the general speed of the program
        self.fpsclock = pygame.time.Clock()

        self.hasGamePad = False
        self.running = True

        print("GamePadController Init")


    def updateGamePad(self, joysticks):

        hasGamePad = joysticks != None

        if not self.hasGamePad and  hasGamePad:
            print("Recognized controller: USB Gamepad ")
            print("basedir: " + str(DATA_DIR))
            self.put_message(GamePadConnected(GamePadControllerProto(joystick_name=joysticks[0].get_name()), "USB Gamepad connected"))


        if  self.hasGamePad and not hasGamePad:
            print("USB Gamepad disconnected, please reconnect")
            self.put_message(GamePadDisconnected(GamePadControllerProto(joystick_name=joysticks[0].get_name()), "USB Gamepad disconnected"))

        # ToDO: do this later with iteration information
        #if not self.hasGamePad and not hasGamePad:
        #    print("No Gamepad recognized, please connect")

        self.hasGamePad = hasGamePad


    def refresh_gamepad(self):

        pygame.joystick.quit()
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        if len(joysticks) >= 1:
            joysticks[0].init()

            if joysticks[0].get_name() != 'USB Gamepad ':
                joysticks = None

            self.updateGamePad(joysticks)

        else:
            joysticks = None

        return joysticks


    def run(self):

        refresh = True
        i = 0
        self.gamepad = self.refresh_gamepad()
        while self.running: # main game loop

            #print(" ...refreshing gamepad... ")

            #if refresh:
            #    self.gamepad = self.refresh_gamepad()
            #print(" ...refreshing gamepad done... ")

            if self.hasGamePad:
                for event in pygame.event.get(): # event handling loop

                    if event.type == JOYBUTTONUP:
                        if event.button == 8:
                            #print("Select Button Pressed")
                            self.put_message(GamePadSelectPressed(GamePadControllerProto(self.gamepad[0].get_name()), "Select Button Pressed"))
                            #self.stop()

                            #sys.exit()
                        if event.button == 0:
                            self.put_message(GamePadXPressed(GamePadControllerProto(self.gamepad[0].get_name()), "X Button Pressed"))
                            #print("X pressed")
                        if event.button == 1:
                            self.put_message(GamePadAPressed(GamePadControllerProto(self.gamepad[0].get_name()), "A Button Pressed"))
                            #print("A pressed")
                        if event.button == 2:
                            self.put_message(GamePadBPressed(GamePadControllerProto(self.gamepad[0].get_name()), "B Button Pressed"))
                            #print("B pressed")
                        if event.button == 3:
                            self.put_message(GamePadYPressed(GamePadControllerProto(self.gamepad[0].get_name()), "Y Button Pressed"))
                            #print("Y pressed")
                        if event.button == 4:
                            self.put_message(GamePadShoulderLPressed(GamePadControllerProto(self.gamepad[0].get_name()), "Left Shoulder Button Pressed"))
                        if event.button == 5:
                            self.put_message(GamePadShoulderRPressed(GamePadControllerProto(self.gamepad[0].get_name()), "Right Shoulder Button Pressed"))
                        if event.button == 9:
                            self.put_message(GamePadStartPressed(GamePadControllerProto(self.gamepad[0].get_name()), "Start Button Pressed"))
                            #print("Start Button Pressed")


                            path = DATA_DIR + "/Portal Sentry - is anyone there.ogg"

                            print("playing file " + path)

                            JumpSound = pygame.mixer.Sound(path)
                            JumpSound.play()


                        #else:
                        #    print(event.button)


                    elif event.type == JOYAXISMOTION:
                        if event.joy == 0 and event.axis == 1 and event.value > 0.5:
                            self.put_message(GamePadDownPressed(GamePadControllerProto(self.gamepad[0].get_name()), "Down Pressed"))

                        if event.joy == 0 and event.axis == 1 and event.value < -0.5:
                            self.put_message(GamePadUpPressed(GamePadControllerProto(self.gamepad[0].get_name()), "Up Pressed"))

                        if event.joy == 0 and event.axis == 0 and event.value > 0.5:
                            self.put_message(GamePadRightPressed(GamePadControllerProto(self.gamepad[0].get_name()), "Right Pressed"))

                        if event.joy == 0 and event.axis == 0 and event.value < -0.5:
                            self.put_message(GamePadLeftPressed(GamePadControllerProto(self.gamepad[0].get_name()), "Left Pressed"))



            #time.sleep(checking_interval)
            i = i +1

            refresh = (i % refresh_cycle == 0 and i > 0)


        return


    def stop(self):
        pygame.quit()
        self.running = False
        self.release()
        Process.terminate(self)

    def start(self):

        pygame.init()
        self.running = True
        Process.start(self)
        print("GamePadController started")

    def release(self):
        pygame.quit()
