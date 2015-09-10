__author__ = 'mithrawnuruodo'

in_memory_database=False
on_raspberry_pi = False

from MessageHandler import MessageBus, Observer
from Messages import NewPrintingTaskMsg
from GamePadController import GamePadController

if on_raspberry_pi:
    from StepperController import StepperController
    from BeamerController import BeamerController
import Server
from Messages import GamePadSelectPressed
#from DataController import DataPool, PrintingTaskController
from DataBaseController import DataBaseController




class SlaPrinterController(Observer):

    def __init__(self):

        self.io_bus = MessageBus()
        self.io_bus.register(self)

        if on_raspberry_pi:
            self.stepperController = StepperController(self.io_bus)

        self.pygameIoController = GamePadController(self.io_bus)



        self.data_bus = MessageBus()
        self.data_bus.register(self)
        self.db_controller = DataBaseController(in_memory_database, bus=self.data_bus)

        if on_raspberry_pi:
            self.pygameRenderController = BeamerController(dispatcher=self.data_bus)

        self.server =  Server.SlaPrinterApp(__name__, db_controller = self.db_controller)



    def start(self):

        # start msg buses
        self.io_bus.start()
        self.data_bus.start()


        self.pygameIoController.start()

        if on_raspberry_pi:
            self.pygameRenderController.start()
            #self.stepperController.start() -> currently not used as process

        self.server.run(host='0.0.0.0',debug=True, port=4242,  use_evalex=False)



    def release(self):

        # stop msg buses
        self.io_bus.stop()
        self.data_bus.stop()

        self.pygameIoController.stop()

        if on_raspberry_pi:
            self.pygameRenderController.stop()
            self.stepperController.stop()

        self.data.stop()


        # stop server
        self.server.stop()




    def notify(self, message):

        if isinstance(message, GamePadSelectPressed):
            self.release()


        if isinstance(message.sender, DataBaseController):
            print("[Controller] :: received message from Database >> " + message.msg)

            if isinstance(message, NewPrintingTaskMsg):
                print("[Controller] :: .... >> received task >> " + str(message.task))

        else:
            print("[Controller] :: " + str(message))

