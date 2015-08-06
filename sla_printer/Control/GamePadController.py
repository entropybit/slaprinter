import random, pygame, sys
from pygame.locals import *
from threading import Thread
from MessageHandler import Observable, Dispatcher
from Messages import GamePadConnected, GamePadDisconnected, GamePadDownPressed, GamePadUpPressed, GamePadStartPressed


pygame.init()

class SnesController(Observable, Thread):

    def __init__(self, dispatcher, fps=30):
        Thread.__init__(self)
        Observable.__init__(self, dispatcher)

        self.fps = 30 # frames per second, the general speed of the program


        self.fpsclock = pygame.time.Clock()
        self.hasGamePad = False




    def updateGamePad(self, joysticks):

        hasGamePad = joysticks != None

        if not self.hasGamePad and  hasGamePad:
            print("Recognized controller: USB Gamepad ")
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


        while True: # main game loop

            self.gamepad = self.refresh_gamepad()

            if self.hasGamePad:
                for event in pygame.event.get(): # event handling loop
                    if event.type == JOYBUTTONUP:
                        if event.button == 9:
                            pygame.quit()
                            sys.exit()
                        if event.button == 2: #closes the program when you press start
                            self.put_message(GamePadUpPressed(self,"Up Button Pressed"))
                        if event.button == 3: #closes the program when you press start
                            self.put_message(GamePadDownPressed(self,"Down Button Pressed"))
                        if event.button == 0: #closes the program when you press start
                            self.put_message(GamePadStartPressed(self,"Start Button Pressed"))
                        else:
                            print(event.button)


                    elif event.type == JOYAXISMOTION:
                        print event.axis
                        print event.value

                #JumpSound = pygame.mixer.Sound('Portal Sentry - is anyone there.ogg')
                #JumpSound.play()
                #pygame.mixer.music.load('Firewell.ogg')
                #pygame.mixer.music.play(-1, 0)


            self.fpsclock.tick(self.fps)


if __name__ == "__main__":
    disp = Dispatcher()
    snes = SnesController(disp)
    snes.start()