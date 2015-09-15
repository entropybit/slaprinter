#!/usr/bin/env python


__author__ = 'mithrawnuruodo'

import pygame, time
import pygame.image, pygame.display
from pygame.locals import *
import Model.Stepper as Stepper
pygame.init()

FPS = 30 # frames per second, the general speed of the program
def main():
    FPSCLOCK = pygame.time.Clock()

    motor = Stepper.SoncebosStepper()

    Belichtungszeit = 600
    scale = 0.8
    main_surface = pygame.display.set_mode((int(1920*scale), int(1080*scale)))
    printingmode = False
    while True: # main game loop

        picture = pygame.image.load("/home/pi/druckerskripte/sla_printer/black.png")
        main_surface.blit(picture, (0, 0))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        if printingmode == True:
            if time.time()-zeit > Belichtungszeit:
                motor.upOneStep()
                zeit = time.time()

#            time.sleep(Belichtungszeit)


if __name__ == '__main__':
    main()
