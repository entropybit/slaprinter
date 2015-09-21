import pygame
from pygame.locals import *
from multiprocessing import Process

from ServiceFunctions import now
#from threading import Thread
import Control.MessageHandler as handler
import Control.Config as conf
import Control.Messages as msg

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
#from Messages import *
import Control.ServiceFunctions as srvfunc

import os



DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/Data"

class PygameControllerProto(object):

    def __init__(self, joystick_name="unknown"):
        self.joystick_name = joystick_name

    def __str__(self):
        return "joystick [" + self.joystick_name + "] found"


class PygameController(handler.Observable, handler.Observer, Process):

    def __init__(self, sending_bus=handler.MessageBus(), receiving_bus=handler.MessageBus()):
        Process.__init__(self)
        handler.Observable.__init__(self, sending_bus)
        handler.Observer.__init__(self, receiving_bus)

        self.FPSCLOCK = pygame.time.Clock()
        self.FPS = 30

        self.hasGamePad = False
        self.disp_black = True
        self.running = True

        print("GamePadController Init")

        #todo: die folgenden konstanten verfuegbar machen (aka den datentransport vom client hierher)
        #self.PlotListX            diese drei objekte heissen in sla_client/Model/slicingModels.py genauso und muessen hier verfuegbar sein
        #self.PlotListY
        #self.sliceNummer = 1
        #self.x_dims
        #self.y_dims

    def updateGamePad(self, joysticks):

        hasGamePad = joysticks != None

        if not self.hasGamePad and  hasGamePad:
            print("Recognized controller: USB Gamepad ")
            print("basedir: " + str(DATA_DIR))
            self.put_message(msg.GamePadConnected(PygameControllerProto(joystick_name=joysticks[0].get_name()), "USB Gamepad connected"))


        if  self.hasGamePad and not hasGamePad:
            print("USB Gamepad disconnected, please reconnect")
            self.put_message(msg.GamePadDisconnected(PygameControllerProto(joystick_name=joysticks[0].get_name()), "USB Gamepad disconnected"))

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

        #if conf.on_raspberry_pi:
        #    self.main_surface = pygame.display.set_mode((int(1920*scale), int(1080*scale)))
        #else:
        self.main_surface = pygame.display.set_mode((int(1024), int(786)))

        while self.running: # main game loop

            if refresh:
               self.gamepad = self.refresh_gamepad()

            if self.disp_black:
                self.display_black(self.main_surface)
            else:
                fig = plt.figure(figsize=[4, 4], dpi=100, facecolor='k')# 100 dots per inch, so the resulting buffer is 400x400 pixels# )
                #ax = fig.gca()
                #plt.subplot(1, 1, 1, axisbg='k')
                #plt.fill(self.PlotArrayX[self.slicenummer], self.PlotArrayY[self.slicenummer], 'white')
                #plt.xlim(self.x_dims)
                #plt.ylim(self.y_dims)

                #canvas = agg.FigureCanvasAgg(fig)
                #canvas.draw()
                #renderer = canvas.get_renderer()
                #raw_data = renderer.tostring_rgb()
                #screen = pygame.display.get_surface()
                #size = canvas.get_width_height()

                #surf = pygame.image.fromstring(raw_data, size, "RGB")
                #screen.blit(self.mainSurface, (0, 0))
                #pygame.display.flip()
                self.update()



            self.event_handling()


            #time.sleep(checking_period)

            i = i +1
            refresh = (i % conf.refresh_cycle == 0 and i > 0)




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

    def display_black(self, surface):
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
                            self.put_message(msg.GamePadSelectPressed(PygameControllerProto(self.gamepad[0].get_name()), "Select Button Pressed"))
                            #self.stop()
                            #sys.exit()

                        if event.button == 0:
                            self.put_message(msg.GamePadXPressed(PygameControllerProto(self.gamepad[0].get_name()), "X Button Pressed"))
                            #print("X pressed")

                        if event.button == 1:
                            self.put_message(msg.GamePadAPressed(PygameControllerProto(self.gamepad[0].get_name()), "A Button Pressed"))
                            #print("A pressed")

                        if event.button == 2:
                            self.put_message(msg.GamePadBPressed(PygameControllerProto(self.gamepad[0].get_name()), "B Button Pressed"))
                            #print("B pressed")

                        if event.button == 3:
                            self.put_message(msg.GamePadYPressed(PygameControllerProto(self.gamepad[0].get_name()), "Y Button Pressed"))
                            #print("Y pressed")

                        if event.button == 4:
                            #self.black()
                            self.put_message(msg.GamePadShoulderLPressed(PygameControllerProto(self.gamepad[0].get_name()), "Left Shoulder Button Pressed"))

                        if event.button == 5:
                            #self.black()
                            self.put_message(msg.GamePadShoulderRPressed(PygameControllerProto(self.gamepad[0].get_name()), "Right Shoulder Button Pressed"))

                        if event.button == 9:
                            self.put_message(msg.GamePadStartPressed(PygameControllerProto(self.gamepad[0].get_name()), "Start Button Pressed"))

                    elif event.type == JOYAXISMOTION:
                        if event.joy == 0 and event.axis == 1 and event.value > 0.5:
                            self.put_message(msg.GamePadDownPressed(PygameControllerProto(self.gamepad[0].get_name()), "Down Pressed"))

                        if event.joy == 0 and event.axis == 1 and event.value < -0.5:
                            self.put_message(msg.GamePadUpPressed(PygameControllerProto(self.gamepad[0].get_name()), "Up Pressed"))

                        if event.joy == 0 and event.axis == 0 and event.value > 0.5:
                            self.put_message(msg.GamePadRightPressed(PygameControllerProto(self.gamepad[0].get_name()), "Right Pressed"))

                        if event.joy == 0 and event.axis == 0 and event.value < -0.5:
                            self.put_message(msg.GamePadLeftPressed(PygameControllerProto(self.gamepad[0].get_name()), "Left Pressed"))



    def black(self):
        #print("disp_black :" + str(self.disp_black))
        self.disp_black = not self.disp_black
        #print("disp_black :" + str(self.disp_black))

        #self.update()


    def update(self):
        pygame.display.update()

    def notify(self, msg):
        print("[" + str(now()) + "] PygameController :: " + str(msg))

if __name__ == "__main__":
    jep = PygameController()
    jep.run()

