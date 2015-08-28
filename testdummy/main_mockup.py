#!/usr/bin/env python


__author__ = 'mithrawnuruodo'

import random, pygame, sys, time
import pygame.image, pygame.display
from pygame.locals import *
import Model.Stepper as Stepper
pygame.init()

FPS = 30 # frames per second, the general speed of the program
def main():
    FPSCLOCK = pygame.time.Clock()

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    joysticks[0].init()

    if joysticks[0].get_name() == 'USB Gamepad ':
        print  "Recognized controller: USB Gamepad "
    else:
        print "Error: did not recognize controller"

    fisch = Stepper.SoncebosStepper()

    scale = 0.8
    main_surface = pygame.display.set_mode((int(1920*scale), int(1080*scale)))
    printingmode = False
    while True: # main game loop

        for event in pygame.event.get(): # event handling loop
            if event.type == JOYBUTTONUP:
                print event
                #if str(event).split()[4][0] == "8":
                    #print "beende programm"
                    #pygame.quit()
                    #sys.exit()
                if str(event).split()[4][0] == "2":
                    fisch.upOneStep()
                if str(event).split()[4][0] == "3":
                    fisch.downOneStep()
                if str(event).split()[4][0] == "9":
                    printingmode = not printingmode
                    if printingmode == True:
                        print("printing started!")
                        JumpSound = pygame.mixer.Sound('hakuna matata.ogg')
                        JumpSound.play()
                    else:
                        print("printing ended!")
                #if str(event).split()[4][0] == "1":
                 #   fisch.down_toEnd()
            elif event.type == JOYAXISMOTION:
                if event.joy ==0 and event.axis == 1 and event.value > 0.5:
                    print("Moving downwards")
                    fisch.downOneStep()
                if event.joy ==0 and event.axis == 1 and event.value < -0.5:
                    print("Moving upwards")
                    fisch.upOneStep()


        if printingmode == True:
            picture = pygame.image.load("/home/pi/druckerskripte/sla_printer/white.png")
            print("moving 1 step")
            fisch.upOneStep()
            time.sleep(3)


        else:
            picture = pygame.image.load("/home/pi/druckerskripte/sla_printer/black.png")
        main_surface.blit(picture, (0, 0))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


"""
def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

        pygame.event.post(event) # put the other KEYUP event objects back
"""
if __name__ == '__main__':
    main()
