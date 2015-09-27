__author__ = 'mithrawnuruodo'

from MessageHandler import Observer, Observable, MessageBus
from Model import SoncebosStepper
from Messages import OneStepDown, OneStepUp, SeveralStepsDown, SeveralStepsUp, SeveralStepsUpAndDown, SeveralStepsDownAndUp
from ServiceFunctions import now
from Messages import GamePadUpPressed, GamePadDownPressed
from Messages import GamePadShoulderLPressed, GamePadShoulderRPressed
from Messages import GamePadLeftPressed, GamePadRightPressed
from Messages import GamePadAPressed, GamePadBPressed


from Config import several_steps, multiplier_base, log_steppercontroller

class StepperControllerProto(object):

    def __init__(self):
        self.stepper = SoncebosStepperProto()

class SoncebosStepperProto(object):


    def __init__(self):
            self.__name = "8660R013"
            self.__version = 1.0

class StepperController(Observer, Observable):

    def __init__(self, bus):
        print("StepperController initializing")
        Observable.__init__(self,bus)
        Observer.__init__(self,bus)
        #Process.__init__(self)

        #self.commands= Queue()


        self.control_bus = MessageBus()
        self.stepper = SoncebosStepper(bus=self.control_bus)
        self.running = False
        self.multiplier = multiplier_base



    def start(self):
        print("StepperController started")
        self.start = False
        #Process.start(self)
        self.control_bus.start()
        self.stepper.start()


    def stop(self):
        self.stepper.stop()
        self.control_bus.stop()


    def notify(self,Message):

        if isinstance(Message, GamePadUpPressed):

            if log_steppercontroller:
                print("[" + str(now()) + "] StepperController :: GamePadUpPressed")

            self.control_bus.put(OneStepUp(StepperControllerProto(), "Move one step upwards"))

        elif isinstance(Message, GamePadLeftPressed):

            if log_steppercontroller:
                print("[" + str(now()) + "] StepperController :: GamePadLeftPressed")

            self.control_bus.put(SeveralStepsDown(StepperControllerProto(), "Move multiple step downwards", self.multiplier*several_steps))


        elif isinstance(Message, GamePadRightPressed):

            if log_steppercontroller:
                print("[" + str(now()) + "] StepperController :: GamePadRightPressed")

            self.control_bus.put(SeveralStepsUp(StepperControllerProto(), "Move multiple steps upwards", self.multiplier*several_steps))


        elif isinstance(Message, GamePadDownPressed):

            if log_steppercontroller:
                print("[" + str(now()) + "] StepperController :: GamePadDownPressed")

            self.control_bus.put(OneStepDown(StepperControllerProto(), "Move one step down"))

        elif isinstance(Message, GamePadShoulderLPressed):

            if log_steppercontroller:
                print("[" + str(now()) + "] StepperController :: GamePadShoulderLPressed")

            self.control_bus.put(SeveralStepsUpAndDown(StepperControllerProto(), "Move multiple steps up and down", self.multiplier*several_steps))

        elif isinstance(Message, GamePadShoulderRPressed):

            if log_steppercontroller:
                print("[" + str(now()) + "] StepperController :: GamePadShoulderRPressed")

            self.control_bus.put(SeveralStepsDownAndUp(StepperControllerProto(), "Move multiple steps down and up", self.multiplier*several_steps))






