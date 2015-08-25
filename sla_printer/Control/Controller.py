__author__ = 'mithrawnuruodo'

from MessageHandler import Dispatcher, Observer
from Messages import GamePadStartPressed
from GamePadController import GamePadController
from StepperController import StepperController
import Server
from Messages import GamePadSelectPressed
from DataController import DataPool, PrintingTaskController
from multiprocessing import Process

class SlaPrinterController(Observer):

    def __init__(self):

        self.io_dispatcher = Dispatcher()
        self.io_dispatcher.register_observer(self)
        self.stepperController = StepperController(self.io_dispatcher)
        self.pygameController = GamePadController(self.io_dispatcher)


        self.data_dispatcher = Dispatcher()
        self.data_dispatcher.register_observer(self)
        self.data = DataPool(dispatcher=self.data_dispatcher)
        self.task_controller = PrintingTaskController(dispatcher=self.data_dispatcher)

        self.server = Process(target=Server.start_flask)

    def start(self):

        self.io_dispatcher.start()
        self.pygameController.start()
        self.data_dispatcher.start()
        self.server.start()


    def release(self):

        self.pygameController.stop()

        self.stepperController.stop()
        self.io_dispatcher.stop()
        self.data_dispatcher.stop()

        # stop server
        self.server.terminate()
        self.server.join()




    def notify(self, message):

        if isinstance(message, GamePadSelectPressed):
            self.release()

        else:
            print("[Controller] :: " + str(message))

