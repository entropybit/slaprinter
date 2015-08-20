__author__ = 'mithrawnuruodo'

from MessageHandler import Dispatcher, Observer
from Messages import GamePadStartPressed
from GamePadController import GamePadController
from StepperController import StepperController
from TesterrController import BeamerController
import Server
from Messages import GamePadSelectPressed
from DataController import DataPool
from multiprocessing import Process

class SlaPrinterController(Observer):

    def __init__(self):

        self.io_dispatcher = Dispatcher()
        self.io_dispatcher.register_observer(self)
        self.stepperController = StepperController(self.io_dispatcher)
        self.pygameController = GamePadController(self.io_dispatcher)
        self.server = Process(target=Server.start_flask)

        self.data_dispatcher = Dispatcher()
        self.data = DataPool(self.data_dispatcher)

    def start(self):

        self.io_dispatcher.start()
        self.pygameController.start()
        #self.stepperController.start()
        #self.beamerController.start()
        self.server.start()


    def release(self):

        self.pygameController.stop()

        self.stepperController.stop()
        self.io_dispatcher.stop()

        # stop server
        self.server.terminate()
        self.server.join()




    def notify(self, message):

        if isinstance(message, GamePadSelectPressed):
            self.release()

