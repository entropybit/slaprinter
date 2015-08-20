import random, pygame, sys
from pygame.locals import *
#from multiprocessing import Process
from threading import Thread
from MessageHandler import Observable, Dispatcher
from Messages import *

import os

DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/Data"



class GamePadController(Observable, Thread):

    def __init__(self, dispatcher, fps=30):
        Thread.__init__(self)
        Observable.__init__(self, dispatcher)

        self.fps = fps # frames per second, the general speed of the program


        self.fpsclock = pygame.time.Clock()
        self.hasGamePad = False
        self.running = True


    def updateGamePad(self, joysticks):

        hasGamePad = joysticks != None

        if not self.hasGamePad and  hasGamePad:
            print("Recognized controller: USB Gamepad ")
            print("basedir: " + str(DATA_DIR))
            self.put_message(GamePadConnected(self, "USB Gamepad connected"))


        if  self.hasGamePad and not hasGamePad:
            print("USB Gamepad disconnected, please reconnect")
            self.put_message(GamePadDisconnected(self, "USB Gamepad disconnected"))

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


        while self.running: # main game loop

            #print(" ...refreshing gamepad... ")
            self.gamepad = self.refresh_gamepad()
            #print(" ...refreshing gamepad done... ")

            if self.hasGamePad:
                for event in pygame.event.get(): # event handling loop

                    if event.type == JOYBUTTONDOWN:
                        if event.button == 8:
                            #print("Select Button Pressed")
                            self.put_message(GamePadSelectPressed(self,"Select Button Pressed"))
                            self.stop()

                            #sys.exit()
                        if event.button == 0:
                            self.put_message(GamePadXPressed(self,"X Button Pressed"))
                            #print("X pressed")
                        if event.button == 1:
                            self.put_message(GamePadAPressed(self,"A Button Pressed"))
                            #print("A pressed")
                        if event.button == 2:
                            self.put_message(GamePadBPressed(self,"B Button Pressed"))
                            #print("B pressed")
                        if event.button == 3:
                            self.put_message(GamePadYPressed(self,"Y Button Pressed"))
                            #print("Y pressed")
                        if event.button == 9:
                            self.put_message(GamePadStartPressed(self,"Start Button Pressed"))
                            #print("Start Button Pressed")


                            path = DATA_DIR + "/Portal Sentry - is anyone there.ogg"

                            #print("playing file " + path)

                            JumpSound = pygame.mixer.Sound(path)
                            JumpSound.play()


                        #else:
                        #    print(event.button)


                    elif event.type == JOYAXISMOTION:
                        print event.axis
                        print event.value

                #JumpSound = pygame.mixer.Sound('Portal Sentry - is anyone there.ogg')
                #JumpSound.play()
                #pygame.mixer.music.load('Firewell.ogg')
                #pygame.mixer.music.play(-1, 0)


            self.fpsclock.tick(self.fps)


    def stop(self):
        pygame.quit()
        self.running = False

    def start(self):

        pygame.init()
        self.running = True
        Thread.start(self)


if __name__ == "__main__":
    disp = Dispatcher()
    snes = GamePadController(disp)
    snes.start()