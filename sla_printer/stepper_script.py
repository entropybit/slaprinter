#!/usr/bin/env python
import time
from abc import ABCMeta, abstractmethod
import argparse
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

class Stepper(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        #self.__step = 0
        self.init_gpio()

    def release(self):
        print("gpio cleanup")
        #GPIO.cleanup()
        print("...done...")

    def init_gpio(self):
        GPIO.setmode(GPIO.BOARD)

class SoncebosStepper(Stepper):

    def __init__(self):
        Stepper.__init__(self)
        self.__name = "8660R013"
        self.__version = 1.0
        #self.__dir = 1.0        # direction ( 0 | cw ) vs ( 1 | ccw )
        #self.__enable = 0.0     # power on 0/1 <--> off/on respectively
        GPIO.setmode(GPIO.BOARD)

        self.directionPin = 16 #cw/ccw - the directional pin (False=cw)
        self.startPin = 18 #move yes/no pwm
        self.enablePin = 22 #enable engine yes/no
        self.detectPinTop = 11
        self.detectPinBottom = 13

	# replace with self.reset() ?
        GPIO.setup(self.directionPin, GPIO.OUT)
        GPIO.output(self.directionPin, False)
        GPIO.setup(self.startPin, GPIO.OUT)
        GPIO.output(self.startPin, False)
        GPIO.setup(self.enablePin, GPIO.OUT)
        GPIO.output(self.enablePin, False)

        GPIO.setup(self.detectPinTop, GPIO.IN)
        GPIO.setup(self.detectPinTop, False)
        GPIO.setup(self.detectPinBottom, False)

        self.secondsToMove =  0.1
        #self.secondsToMove =  0.086956522
        self.frequency_slow = 5000 #5000Hz @ 20s = 2,3cm

    def __str__(self):
        return self.__name + " version " + str(self.__version)

    def upOneStep(self):
        if GPIO.input(self.detectPinTop) == False:
            GPIO.output(self.directionPin, True)
            GPIO.output(self.enablePin, False)
            pwm = GPIO.PWM(self.startPin, self.frequency_slow) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
            pwm.start(50) #number is percentage of duty cycle: 1-50 works without problems or differences
            time.sleep(self.secondsToMove) #number is seconds to go up
            GPIO.output(self.enablePin, True)

    def downOneStep(self):
        if GPIO.input(self.detectPinBottom) == False:
            GPIO.output(self.directionPin, False)
            GPIO.output(self.enablePin, False)
            pwm = GPIO.PWM(self.startPin, self.frequency_slow) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
            pwm.start(50) #number is percentage of duty cycle: 1-50 works without problems or differences
            time.sleep(self.secondsToMove) #number is seconds to go up
            GPIO.output(self.enablePin, True)

    def upOneStepManual(self):
        if GPIO.input(self.detectPinTop) == False:
            GPIO.output(self.directionPin, True)
            GPIO.output(self.enablePin, False)
            pwm = GPIO.PWM(self.startPin, 5000) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
            pwm.start(50) #number is percentage of duty cycle: 1-50 works without problems or differences
            time.sleep(self.secondsToMove) #number is seconds to go up
            GPIO.output(self.enablePin, True)
	self.reset()

    def downOneStepManual(self):
        if GPIO.input(self.detectPinBottom) == False:
            GPIO.output(self.directionPin, False)
            GPIO.output(self.enablePin, False)
            pwm = GPIO.PWM(self.startPin, 5000) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
            pwm.start(50) #number is percentage of duty cycle: 1-50 works without problems or differences
            time.sleep(self.secondsToMove) #number is seconds to go up
            GPIO.output(self.enablePin, True)
	self.reset()


    def up_toEnd(self):
        GPIO.output(self.directionPin, True)
        GPIO.output(self.enablePin, False)
        while not GPIO.input(self.detectPinTop) or not GPIO.input(self.detectPinBottom):
            GPIO.output(self.startPin, True)
            GPIO.output(self.startPin, False)
            print  #why the fuck does this run so friggin fast? faster than the fastest pwm. this shouldnt be possible. how?
        GPIO.output(self.enablePin, True)

    def down_toEnd(self):
        GPIO.output(self.directionPin, False)
        GPIO.output(self.enablePin, False)
        while not GPIO.input(self.detectPinTop) or not GPIO.input(self.detectPinBottom):
            GPIO.output(self.startPin, True)
            GPIO.output(self.startPin, False)
            print  #why the fuck does this run so friggin fast? faster than the fastest pwm. this shouldnt be possible. how?
        GPIO.output(self.enablePin, True)

    def down_ssh_manual(self):
        GPIO.output(self.directionPin, False)
        GPIO.output(self.enablePin, False)
        pwm = GPIO.PWM(self.startPin, self.frequency_slow) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
        pwm.start(50) #zahl ist prozentualer duty cycle 1-50 geht ohne unterschied
        raw_input("Press return to stop going down...")
        pwm.stop()
        GPIO.output(self.enablePin, True)

    def up_ssh_manual(self):
        GPIO.output(self.directionPin, True)
        GPIO.output(self.enablePin, False)
        pwm = GPIO.PWM(self.startPin, self.frequency_slow) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
        pwm.start(50) #zahl ist prozentualer duty cycle 1-50 geht ohne unterschied
        raw_input("Press return to stop going down...")
        pwm.stop()
        GPIO.output(self.enablePin, True)
	
    def reset_pins(self):
        GPIO.setup(self.directionPin, GPIO.OUT)
        GPIO.output(self.directionPin, False)
        GPIO.setup(self.startPin, GPIO.OUT)
        GPIO.output(self.startPin, False)
        GPIO.setup(self.enablePin, GPIO.OUT)
        GPIO.output(self.enablePin, False)

        GPIO.setup(self.detectPinTop, GPIO.IN)
        GPIO.setup(self.detectPinTop, False)
        GPIO.setup(self.detectPinBottom, False)    



parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('steps', metavar='steps', type=int,help='The number of steps')
parser.add_argument('--down', action='store_true', default=False, help='step downwards')
parser.add_argument('--updown', action='store_true', default=False, help='move up and down again')
parser.add_argument('--downup', action='store_true', default=False, help='move down and up again' )

results = parser.parse_args()

#print("results " + str(results))

steps = results.steps
down = results.down
updown = results.updown
downup = results.downup

stepper = SoncebosStepper()


if not updown and not downup:

    if not down:
        print("stepping " + str(steps) + " up")
        for i in range(steps):
            stepper.upOneStep()
	    time.sleep(0.0001)


    else:
        print("stepping " + str(steps) + " down")
        for i in range(steps):
            stepper.downOneStep()
	    time.sleep(0.0001)


if updown and not downup:

    print("stepping " + str(steps) + " up")
    for i in range(steps):
        stepper.upOneStep()
	time.sleep(0.0001)

    print("stepping " + str(steps) + " down")
    for i in range(steps):
        stepper.downOneStep()
	time.sleep(0.0001)




if not updown and downup:

    print("stepping " + str(steps) + " down")
    for i in range(steps):
        stepper.downOneStep()
	time.sleep(0.0001)

    print("stepping " + str(steps) + " up")
    for i in range(steps):
        stepper.upOneStep()
	time.sleep(0.0001)

