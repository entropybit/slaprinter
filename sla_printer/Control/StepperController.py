__author__ = 'mithrawnuruodo'

from MessageHandler import Observer, Observable, MessageBus
from Model import SoncebosStepper
from Messages import OneStepDown, OneStepUp, SeveralStepsDown, SeveralStepsUp, SeveralStepsUpAndDown
from ServiceFunctions import now
from multiprocessing import Process, Queue
from Messages import GamePadUpPressed, GamePadDownPressed, GamePadShoulderLPressed, GamePadShoulderRPressed


from Config import  mode,multiple_steps

class StepperController(Observer, Observable, Process):

    def __init__(self, bus):
        Observable.__init__(self,bus)
        Observer.__init__(self,bus)

        self.commands= Queue()

        self.stepper = SoncebosStepper()
        self.running = False

        print("stepper created")


    def start(self):
        self.start = False
        Process.start()


    def stop(self):
        self.stepper.release()


    def run(self):

        while self.running:

            while not self.commands.empty():

                command = self.commands.get()

                #OneStepDown, OneStepUp, SeveralStepsDown, SeveralStepsUp, SeveralStepsUpAndDown
                if isinstance(command, OneStepDown):
                    self.stepper.downOneStep()

                elif isinstance(command, OneStepUp):
                    self.stepper.upOneStep()

                elif isinstance(command, SeveralStepsUp):
                    for i in range(multiple_steps):
                        self.stepper.upOneStep()

                elif isinstance(command, SeveralStepsDown):
                    for i in range(multiple_steps):
                        self.stepper.downOneStep()

                elif isinstance(command, SeveralStepsUpAndDown):
                    for i in range(multiple_steps):
                        self.stepper.upOneStep()

                    for i in range(multiple_steps):
                        self.stepper.downOneStep()




    def notify(self,Message):
         print("[" + str(now()) + "] stepper :: " + str(Message.msg))

         if mode == "stepper_calibration":

             #GamePadUpPressed, GamePadDownPressed, GamePadShoulderLPressed, GamePadShoulderRPressed

             if isinstance(Message, GamePadUpPressed):
                 self.commands.put(OneStepUp(self, "Move one step upwards"))

             if isinstance(Message, GamePadDownPressed):
                self.commands.put(OneStepDown(self, "Move one step downwards"))


             if isinstance(Message, GamePadShoulderLPressed):
                self.commands.put(SeveralStepsUp(self, "Move multiple steps upwards"))

             if isinstance(Message, GamePadShoulderRPressed):
                self.commands.put(SeveralStepsDown(self, "Move multiple steps downwards"))







