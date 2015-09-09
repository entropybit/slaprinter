__author__ = 'mithrawnuruodo'

on_raspberry_pi = False

from MessageHandler import MessageBus, Observer
from Messages import GamePadStartPressed
from GamePadController import GamePadController

if on_raspberry_pi:
    from StepperController import StepperController
    from BeamerController import BeamerController
import Server
from Messages import GamePadSelectPressed
#from DataController import DataPool, PrintingTaskController
from multiprocessing import Process

class SlaPrinterController(Observer):

    def __init__(self):

        self.io_bus = MessageBus()
        self.io_bus.register_observer(self)

        if on_raspberry_pi:
            self.stepperController = StepperController(self.io_bus)

        self.pygameIoController = GamePadController(self.io_bus)



        self.data_bus = MessageBus()

        print("initialized data_dispatcher : " + str(self.data_bus))
        self.data_bus.register_observer(self)
        self.data = DataPool(dispatcher=self.data_bus)
        self.task_controller = PrintingTaskController(dispatcher=self.data_bus)


        if on_raspberry_pi:
            self.pygameRenderController = BeamerController(dispatcher=self.data_bus)

        self.server = Process(target=Server.start_flask)



    def start(self):

        # start msg buses
        self.io_bus.start()
        self.data_bus.start()

        self.task_controller.start()
        self.data.start()


        self.pygameIoController.start()

        if on_raspberry_pi:
            self.pygameRenderController.start()

        self.server.start()



    def release(self):

        # stop msg buses
        self.io_bus.stop()
        self.data_bus.stop()

        self.pygameIoController.stop()

        if on_raspberry_pi:
            self.pygameRenderController.stop()
            self.stepperController.stop()

        self.task_controller.stop()
        self.data.stop()


        # stop server
        self.server.terminate()
        self.server.join()




    def notify(self, message):

        if isinstance(message, GamePadSelectPressed):
            self.release()

        else:
            print("[Controller] :: " + str(message))

