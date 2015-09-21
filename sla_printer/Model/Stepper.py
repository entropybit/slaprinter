__author__ = 'mithrawnuruodo'

import time
from abc import ABCMeta, abstractmethod
import Control as cntrl
from multiprocessing import Process, Queue

stepper_processing_period = cntrl.Config.stepper_processing_period
now = cntrl.ServiceFunctions.now
logging = cntrl.Config.log_stepper
stepper_mode = cntrl.Config.stepper_mode


if stepper_mode:
    try:
        import pigpio
    except:
        stepper_mode = False




class Stepper(cntrl.MessageHandler.Observer, Process):
    __metaclass__ = ABCMeta

    def __init__(self, bus):
        cntrl.Observer.__init__(self, bus=bus)
        Process.__init__(self)
        #self.__step = 0

        if stepper_mode:
    	    self._pi = pigpio.pi()
        self._running = False
        self._queue = Queue()

    def release(self):
        print("RPIO cleanup")
        self.reset()
        print("...done...")

    @abstractmethod
    def reset(self):
        pass


class SoncebosStepper(Stepper):

    def __init__(self, bus):
        Stepper.__init__(self, bus)
        self.__name = "8660R013"
        self.__version = 1.0
        #self.__dir = 1.0        # direction ( 0 | cw ) vs ( 1 | ccw )
        #self.__enable = 0.0     # power on 0/1 <--> off/on respectivel

        self.directionPin = 23 #cw/ccw - the directional pin (False=cw)
        self.startPin = 24 #move yes/no pwm
        self.enablePin = 22 #enable engine yes/no
        self.detectPinTop = 17
        self.detectPinBottom = 27
        self.secondsToMove =  0.1
        self.frequency_slow = 5000 #5000Hz @ 20s = 2,3cm

    def reset(self):
        self._pi.write(self.directionPin, 0)
        self._pi.write(self.startPin, 0)
        self._pi.write(self.enablePin, 0)
        self._pi.write(self.detectPinTop, 0)
        self._pi.write(self.detectPinBottom, 0)

    def start(self):
        print("SoncebosStepper starting")


        if stepper_mode:
            self._pi.set_mode(self.directionPin, pigpio.OUTPUT)
            self._pi.set_mode(self.startPin, pigpio.OUTPUT)
            self._pi.set_mode(self.enablePin, pigpio.OUTPUT)
            self._pi.set_mode(self.detectPinTop, pigpio.INPUT)
            self._pi.set_mode(self.detectPinBottom, pigpio.INPUT)
            self.reset()
            print(self._pi.get_PWM_frequency(self.startPin))

        self._running = True
        Process.start(self)

    def __str__(self):
        return self.__name + " version " + str(self.__version)

    def upOneStep(self):

        if stepper_mode:

            top_is_hit = bool(int(self._pi.read(self.detectPinTop)))
            self._pi.set_pull_up_down(self.detectPinTop, pigpio.PUD_DOWN)
            #print(" top_is_hit ? : " + str(top_is_hit))
            if not top_is_hit:
                #print("moving up")
                self._pi.write(self.directionPin, 1)
                self._pi.write(self.enablePin, 0)
                #pwm = RPIO.PWM(self.startPin, self.frequency_slow) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
                #pwm.start(50) #number is percentage of duty cycle: 1-50 works without problems or differences
                self._pi.set_PWM_frequency(self.startPin,self.frequency_slow)
                #print("setted frequency :" + str(self._pi.get_PWM_frequency(self.startPin)))
                self._pi.set_PWM_dutycycle(self.startPin, 128) # PWM 1/2 on
                time.sleep(self.secondsToMove) #number is seconds to go up
                self._pi.set_PWM_dutycycle(self.startPin, 0) # PWM 1/2 on -> reset
                # self.reset()
                self._pi.write(self.enablePin, 1)

        else:
            print("      >>       DUMMY :: up one step")

    def downOneStep(self):

        if stepper_mode:
            down_is_hit = bool(int(self._pi.read(self.detectPinBottom)))
            self._pi.set_pull_up_down(self.detectPinBottom, pigpio.PUD_DOWN)
            #print(" down_is_hit ? : " + str(down_is_hit))
            if not down_is_hit:
            #print("moving down")
                self._pi.write(self.directionPin, 0)
                self._pi.write(self.enablePin, 0)
                #pwm = RPIO.PWM(self.startPin, self.frequency_slow) #last parameter is frequency in Hz, max 70kHz in Python (according to the interwebs)
                #pwm.start(50) #number is percentage of duty cycle: 1-50 works without problems or differences
                self._pi.set_PWM_frequency(self.startPin,self.frequency_slow)
                self._pi.set_PWM_dutycycle(self.startPin, 128) # PWM 1/2 on
                time.sleep(self.secondsToMove) #number is seconds to go up
                self._pi.set_PWM_dutycycle(self.startPin, 0) # PWM 1/2 on -> reset
                self.reset()
                #self._pi.set_pull_up_down(self.enablePin, pigpio.PUD_UP)
                self._pi.write(self.enablePin, 1)
        else:
            print("      >>       DUMMY :: down one step")

    def downSeveralSteps(self, steps):

        if stepper_mode:

            for i in range(steps):
                self.downOneStep()

        else:
            print("      >>       DUMMY :: down several steps")

    def upSeveralSteps(self, steps):

        if stepper_mode:

            for i in range(steps):
                self.upOneStep()

        else:
            print("      >>       DUMMY :: up several steps")



    def upDownSeveralSteps(self, steps):

        if stepper_mode:

            for i in range(steps):
                self.upOneStep()

            for i in range(steps):
                self.downOneStep()

        else:
            print("      >>       DUMMY :: upDownSeveralSteps")


    def up_toEnd(self):

        if stepper_mode:
            for i in range(600):
                self.upOneStep()
        else:
            print("      >>       DUMMY :: up to end")

    def down_toEnd(self):

        if stepper_mode:
            for i in range(600):
                self.downOneStep()
        else:
            print("      >>       DUMMY :: down to end")


    def run(self):

        while self._running:

            while not self._queue.empty():

                msg = self._queue.get()

                if isinstance(msg, cntrl.Messages.OneStepDown):
                    print("[" + str(now()) + "] SoncebosStepper :: moving one step down")
                    self.downOneStep()

                elif isinstance(msg, cntrl.Messages.OneStepUp):
                    print("[" + str(now()) + "] SoncebosStepper :: moving one step up")
                    self.upOneStep()

                elif isinstance(msg, cntrl.Messages.SeveralStepsDown):
                    print("[" + str(now()) + "] SoncebosStepper :: moving multiple steps down")
                    self.downSeveralSteps(msg.steps)

                elif isinstance(msg, cntrl.Messages.SeveralStepsUp):
                    print("[" + str(now()) + "] SoncebosStepper :: moving multiple steps up")
                    self.upSeveralSteps(msg.steps)

                elif isinstance(msg, cntrl.Messages.SeveralStepsUpAndDown):
                    print("[" + str(now()) + "] SoncebosStepper :: moving multiple steps down")
                    self.upDownSeveralSteps(msg.steps)
                else:
                    print("[" + str(now()) + "] SoncebosStepper :: invalid command")

            time.sleep(0.0001)

    def notify(self, msg):
        #from StepperMessages import OneStepDown, OneStepUp, SeveralStepsDown, SeveralStepsUp, SeveralStepsUpAndDown

        if isinstance(msg, cntrl.Messages.OneStepDown):
            print("[" + str(now()) + "] SoncebosStepper :: OneStepDown entering queue")
            #self.downOneStep()
            self._queue.put(msg)

        if isinstance(msg, cntrl.Messages.OneStepUp):
            print("[" + str(now()) + "] SoncebosStepper :: OneStepUp entering queue")
            #self.upOneStep()
            self._queue.put(msg)

        if isinstance(msg, cntrl.Messages.SeveralStepsDown):
            print("[" + str(now()) + "] SoncebosStepper :: SeveralStepsDown entering queue")
            #self.downSeveralSteps(msg.steps)
            self._queue.put(msg)

        if isinstance(msg, cntrl.Messages.SeveralStepsUp):
            print("[" + str(now()) + "] SoncebosStepper :: SeveralStepsUp entering queue")
            #self.upSeveralSteps(msg.steps)
            self._queue.put(msg)

        if isinstance(msg, cntrl.Messages.SeveralStepsUpAndDown):
            #self.upDownSeveralSteps(msg.steps)
            print("[" + str(now()) + "] SoncebosStepper :: SeveralStepsUpAndDown entering queue")
            self._queue.put(msg)

        #else:
        #    print("[SoncebosStepper] :: msg not interpreted as stepper command")

        #print(msg.msg)



if __name__ == "__main__":
    yep = SoncebosStepper()
    yep.upOneStepManual()
