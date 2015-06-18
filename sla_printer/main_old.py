__author__ = 'mithrawnuruodo'

import Model.Stepper as Stepper
import RPi.GPIO as GPIO
#import Control.snes as snes
import View.Beamer as Beamer


#display = View.Beamer()
#display2 = Beamer("pimpstick.svg")

#controller = snes.InputManager()


#fisch = Stepper.SoncebosStepper()
#fisch.down()
#fisch.up()
#fisch.disable()

import random, pygame, sys
from pygame.locals import *

pygame.init()

FPS = 60 # frames per second, the general speed of the program
def main():
    #global FPSCLOCK
    FPSCLOCK = pygame.time.Clock()

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    joysticks[0].init()

    if joysticks[0].get_name() == 'USB Gamepad ':
        print  "Recognized controller: USB Gamepad "
    else:
        print "Error: did not recognize controller"

    fisch = Stepper.SoncebosStepper()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == JOYBUTTONUP:
                print str(event).split()[4][0]
                if str(event).split()[4][0] == "9": #closes the program when you press start
                    pygame.quit()
                    sys.exit()
                if str(event).split()[4][0] == "2": #closes the program when you press start
                    fisch.up()
                if str(event).split()[4][0] == "3": #closes the program when you press start
                    fisch.down()
                if str(event).split()[4][0] == "0": #closes the program when you press start
                    fisch.laser()
                    print "laser ended"


            elif event.type == JOYAXISMOTION:
                print "das war eine achse"
                #print event
                JumpSound = pygame.mixer.Sound('Portal Sentry - is anyone there.ogg')
                JumpSound.play()
                #pygame.mixer.music.load('Firewell.ogg')
                #pygame.mixer.music.play(-1, 0)

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
