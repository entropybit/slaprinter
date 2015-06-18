__author__ = 'mithrawnuruodo'

import time
from abc import ABCMeta, abstractmethod

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


class Stepper(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        #self.__step = 0
        self.init_gpio()


    def __del__(self):
        GPIO.cleanup()

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

        self.laserPin = 7
        self.directionPin = 16 #cw/ccw - the directional pin (False=cw)
        self.startPin = 18 #move yes/no pwm
        self.enablePin = 22 #enable engine yes/no
        GPIO.setup(self.directionPin, GPIO.OUT)
        GPIO.setup(self.startPin, GPIO.OUT)
        GPIO.setup(self.enablePin, GPIO.OUT)
        GPIO.setup(self.laserPin, GPIO.OUT)

    def __str__(self):
        return self.__name + " version " + str(self.__version)

    def enable(self):
        self.__enable = True
        GPIO.output(self.enablePin, True)

    def disable(self):
        self.__enable = False
        GPIO.output(self.enablePin, False)

    def up(self):
        GPIO.output(self.directionPin, False)

        amount_of_pulses = float(9200) #mit 1s auf 9200Hz dreht es sich ca 1mal herum. mit 2s und 4600Hz dreht es sich 1.5mal. wtf
        t = float(1)
        frequency = amount_of_pulses/t

        pwm = GPIO.PWM(self.startPin, frequency) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
        pwm.start(50) #zahl ist prozentualer duty cycle 1-50 geht ohne unterschied
        f = time.clock()
        while 1:
            if time.clock() - f > t:
                pwm.stop()
                break

    def down(self):
        GPIO.output(self.directionPin, True)

        amount_of_pulses = float(1000) #mit 1s auf 9200Hz dreht es sich ca 1mal herum. mit 2s und 4600Hz dreht es sich 1.5mal. wtf
        t = float(1)
        frequency = amount_of_pulses/t

        pwm = GPIO.PWM(self.startPin, frequency) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
        print "pwm start"
        pwm.start(50)
        #zahl ist prozentualer duty cycle 1-50 geht ohne unterschied
        time.sleep(20)
        print "done."
        #f = time.clock()
        #while 1:
         #   if time.clock() - f > t:
          #      pwm.stop()
           #     break

    def laser(self):
        GPIO.output(self.laserPin, True)
        t = float(1)
        f = time.clock()
        while 1:
            if time.clock() - f > t:
                GPIO.output(self.laserPin, False)
                break



#todo: mit 1s auf 9200Hz dreht es sich ca 1mal herum. mit 2s und 4600Hz dreht es sich 1.5mal. wtf
        """     1s 1turn
                2s 1.5turns
                4s 1.8 turns
                10s 2.3 turns
                20s 3.6 turns
        """
#todo: find out why enable pin is always enabled

    def up_wtf(self):
        freq = 1000.0
        print (1.0/(freq*2.0))
        GPIO.output(self.directionPin, False)
        while 1:
            GPIO.output(self.startPin, True)
            #time.sleep(1.0/(freq*2.0))
            GPIO.output(self.startPin, False)
            #time.sleep(1.0/(freq*2.0))
#            print time #why the fuck does this run so friggin fast? faster than the fastest pwm. this shouldnt be possible. how?

#todo: #why the fuck does this run so friggin fast? faster than the fastest pwm. this shouldnt be possible. how?
"""
    def down(self):
        GPIO.output(self.directionPin, True)

        pwm = GPIO.PWM(self.startPin, 1000) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
        pwm.start(50) #zahl ist prozentualer duty cycle 1-50 geht ohne unterschied
        raw_input("Press return to stop going down:")
        pwm.stop()

    def toStart(self):
        pass

    def toEnd(self):
        pass
"""


"""
    def up2(self): #probieren verschiedener frequenzen -  nichts geht. warum? WEIL time.sleep() keine werte unter 1/1000 annimmt. shit.
        GPIO.output(self.directionPin, False)
        for freq in range(1, 21):
            f = time.clock()
            freq = freq
            print "frequenz ist: " + str(freq)
            while 1:
                GPIO.output(self.startPin, True)
                time.sleep(1/(freq*2))
                GPIO.output(self.startPin, False)
                time.sleep(1/(freq*2))
#                print "asd"
                if time.clock() - f > 1:
                    break
"""
