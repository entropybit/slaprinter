__author__ = 'mithrawnuruodo'

import Model.Stepper as Stepper
import Control.snes as snes
#import View.Beamer


#display = View.Beamer("pimpstick.svg")
#display2 = Beamer("pimpstick.svg")
#controller = snes.InputManager()
#fisch = Stepper.SoncebosStepper()
#fisch.down()

import random, pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30 # frames per second, the general speed of the program
def main():
    #global FPSCLOCK
    FPSCLOCK = pygame.time.Clock()

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    joysticks[0].init()

    if joysticks[0].get_name() == 'USB Gamepad ':
        print "Recognized controller: USB Gamepad "
    else:
        print "Error: did not recognize controller"

    Motor = Stepper.SoncebosStepper()

    while True:
        for event in pygame.event.get(): # event handling loop
            if event.type == JOYBUTTONUP:
                if event.button == 9:
                    pygame.quit()
                    sys.exit()
#                if event.button == 0:
#                    display = Beamer()
                if event.button == 1:
                    JumpSound = pygame.mixer.Sound('Portal Sentry - is anyone there.ogg')
                    JumpSound.play()

                else:
                    print(event.button)

            elif event.type == JOYAXISMOTION:
                if event.axis == 1 and event.value > 0.5:
                    print "unne"
                    Motor.downOneStep()
                if event.axis == 1 and event.value < -0.5:
                    print "obbe"
                    Motor.upOneStep()
                if event.axis == 0 and event.value > 0.5:
                    print "rechts"
                if event.axis == 0 and event.value < -0.5:
                    print "links"


#                JumpSound = pygame.mixer.Sound('Portal Sentry - is anyone there.ogg')
#                JumpSound.play()
                #pygame.mixer.music.load('Firewell.ogg')
                #pygame.mixer.music.play(-1, 0)

            FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
