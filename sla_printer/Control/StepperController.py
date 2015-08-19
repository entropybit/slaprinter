__author__ = 'mithrawnuruodo'

from MessageHandler import Observer
from Model import SoncebosStepper

class StepperController(Observer):

    def __init__(self, dispatcher):

        self.dispatcher = dispatcher
        self.dispatcher.register_observer(self)
        self.stepper = SoncebosStepper()