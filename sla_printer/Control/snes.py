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
        print  "Recognized controller: USB Gamepad "
    else:
        print "Error: did not recognize controller"

    while True: # main game loop

        #checkForQuit()

        for event in pygame.event.get(): # event handling loop
            if event.type == JOYBUTTONUP:
                button = event.button
                if button == 9:
                    pygame.quit()
                    sys.exit()
                else:
                    print(button)

                #print str(event).split()[4][0]
                #if str(event).split()[4][0] == "9": #closes the program when you press start
                #    pygame.quit()
                #    sys.exit()

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
