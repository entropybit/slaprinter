__author__ = 'mithrawnuruodo'

import random, pygame, sys
from pygame.locals import *
#from multiprocessing import Process
from threading import Thread
from MessageHandler import Observer, MessageBus
from Messages import *
import time
import Control

import os

DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/Data"



class BeamerController(Thread, Observer):

    def __init__(self, fps=30, bus=MessageBus()):
        Thread.__init__(self)

        self.fps = fps # frames per second, the general speed of the program
        self.bus=bus
        self.bus.register_observer(self)


        self.fpsclock = pygame.time.Clock()
        self.hasGamePad = False
        self.running = True

        self.task_controller = Control.PrintingTaskController()
        self.data_pool = Control.DataPool()

    def run(self):

        scale = 0.8
        pygame.mouse.set_visible(False)
        main_surface = pygame.display.set_mode((int(1920*scale), int(1080*scale)))
        printingmode = False

        while self.running: # main game loop

            #print('#######################################')
            #print(self.data_pool)
            #print(self.data_pool.get_data())
            #print(self.task_controller)
            #print(self.task_controller.active_job())
            #print("")
            #print("")

            task = self.task_controller.active_job()
            #print("task " + str(task))

            if task is not None:
                picture = self.display_task(task,main_surface)
            else:
                picture = self.display_blank(main_surface)


           #self.fpsclock.tick(self.fps)

    def display_task(self, task, surface):

        print("within display_task")
        print("called with task " + str(task))

        illum_time = task['illumination_time']
        slices = task['slices']
        #slices_todo = task['slices_todo']

        i = 0
        for slice in slices:
            print("i = " +str(i))
            print(slice)
            picture = pygame.image.load(DATA_DIR + "/white.png")
            surface.blit(picture, (0, 0))
            time.sleep(illum_time)

            task.slices_todo[i] = True
            i = i+1



    def display_blank(self, surface):
        picture = pygame.image.load(DATA_DIR + "/black.png")
        surface.blit(picture, (0, 0))
        self.fpsclock.tick(self.fps)

    def stop(self):
        pygame.quit()
        self.running = False

    def start(self):

        pygame.init()
        self.running = True
        Thread.start(self)

    def notify(self, msg):

        print("beamer received message: " + str(msg))


#if __name__ == "__main__":
    #beamer = BeamerController()
    #beamer.start()
