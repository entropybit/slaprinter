import random, pygame, sys
from pygame.locals import *
from multiprocessing import Process
#from threading import Thread
from MessageHandler import Observable, MessageBus, Observer
from Controller import on_raspberry_pi
from Messages import *
from Config import checking_interval, refresh_cycle
from ServiceFunctions import now
import os
import time


DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/Data"

class PygameControllerProto(object):

    def __init__(self, joystick_name="unknown"):
        self.joystick_name = joystick_name
        self.main_surface = None

    def __str__(self):
        return "joystick [" + self.joystick_name + "] found"


class PygameController(Observable, Observer, Process):

    def __init__(self, sending_bus=MessageBus(), receiving_bus=MessageBus()):
        Process.__init__(self)
        Observable.__init__(self, sending_bus)
        Observer.__init__(self, receiving_bus)

        self.hasGamePad = False
        self.disp_black = False
        self.running = True

        print("GamePadController Init")


    def updateGamePad(self, joysticks):

        hasGamePad = joysticks != None

        if not self.hasGamePad and  hasGamePad:
            print("Recognized controller: USB Gamepad ")
            print("basedir: " + str(DATA_DIR))
            self.put_message(GamePadConnected(PygameControllerProto(joystick_name=joysticks[0].get_name()), "USB Gamepad connected"))


        if  self.hasGamePad and not hasGamePad:
            print("USB Gamepad disconnected, please reconnect")
            self.put_message(GamePadDisconnected(PygameControllerProto(joystick_name=joysticks[0].get_name()), "USB Gamepad disconnected"))

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

        scale = 0.8
        pygame.mouse.set_visible(False)
        pygame.event.pump()

        if on_raspberry_pi:
            self.main_surface = pygame.display.set_mode((int(1920*scale), int(1080*scale)))
        else:
            self.main_surface = pygame.display.set_mode((int(1024), int(786)))


        while self.running: # main game loop

            #print(" ...refreshing gamepad... ")

            if refresh:
               self.gamepad = self.refresh_gamepad()

            if self.disp_black:
                #print("displaying black screen")
                self.display_blank(self.main_surface)
            else:
                #print("displaying white screen")
                self.display_white(self.main_surface)
            #print(" ...refreshing gamepad done... ")



            self.event_handling()


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

    def display_blank(self, surface):
        black = (0,0,0)
        self.main_surface.fill(black)
        self.update()

    def display_white(self, surface):
        white = (255,255,255)
        self.main_surface.fill(white)
        self.update()
        #picture = pygame.image.load(DATA_DIR + "/white.png")
        #surface.blit(picture, (0, 0))


    def event_handling(self):

        if self.hasGamePad:
                for event in pygame.event.get(): # event handling loop

                    if event.type == JOYBUTTONUP:
                        if event.button == 8:
                            #print("Select Button Pressed")
                            self.put_message(GamePadSelectPressed(PygameControllerProto(self.gamepad[0].get_name()), "Select Button Pressed"))
                            #self.stop()

                            #sys.exit()
                        if event.button == 0:
                            self.put_message(GamePadXPressed(PygameControllerProto(self.gamepad[0].get_name()), "X Button Pressed"))
                            #print("X pressed")
                        if event.button == 1:
                            self.put_message(GamePadAPressed(PygameControllerProto(self.gamepad[0].get_name()), "A Button Pressed"))
                            #print("A pressed")
                        if event.button == 2:
                            self.put_message(GamePadBPressed(PygameControllerProto(self.gamepad[0].get_name()), "B Button Pressed"))
                            #print("B pressed")
                        if event.button == 3:
                            self.put_message(GamePadYPressed(PygameControllerProto(self.gamepad[0].get_name()), "Y Button Pressed"))
                            #print("Y pressed")
                        if event.button == 4:
                            self.black()
                            self.put_message(GamePadShoulderLPressed(PygameControllerProto(self.gamepad[0].get_name()), "Left Shoulder Button Pressed"))
                        if event.button == 5:
                            self.black()
                            self.put_message(GamePadShoulderRPressed(PygameControllerProto(self.gamepad[0].get_name()), "Right Shoulder Button Pressed"))
                        if event.button == 9:
                            self.put_message(GamePadStartPressed(PygameControllerProto(self.gamepad[0].get_name()), "Start Button Pressed"))
                            #print("Start Button Pressed")
                            #path = DATA_DIR + "/Portal Sentry - is anyone there.ogg"
                            #print("playing file " + path)
                            #JumpSound = pygame.mixer.Sound(path)
                            #JumpSound.play()

                    elif event.type == JOYAXISMOTION:
                        if event.joy == 0 and event.axis == 1 and event.value > 0.5:
                            self.put_message(GamePadDownPressed(PygameControllerProto(self.gamepad[0].get_name()), "Down Pressed"))

                        if event.joy == 0 and event.axis == 1 and event.value < -0.5:
                            self.put_message(GamePadUpPressed(PygameControllerProto(self.gamepad[0].get_name()), "Up Pressed"))

                        if event.joy == 0 and event.axis == 0 and event.value > 0.5:
                            self.put_message(GamePadRightPressed(PygameControllerProto(self.gamepad[0].get_name()), "Right Pressed"))

                        if event.joy == 0 and event.axis == 0 and event.value < -0.5:
                            self.put_message(GamePadLeftPressed(PygameControllerProto(self.gamepad[0].get_name()), "Left Pressed"))



    def black(self):
        #print("disp_black :" + str(self.disp_black))
        self.disp_black = not self.disp_black
        #print("disp_black :" + str(self.disp_black))

        #self.update()


    def update(self):
        pygame.display.update()

    def notify(self, msg):


        print("[" + str(now()) + "] PygameController :: " + str(msg))