__author__ = 'mithrawnuruodo'

in_memory_database=False
on_raspberry_pi = False

from MessageHandler import MessageBus, Observer
from Messages import NewPrintingTaskMsg, QuitMessage
from GamePadController import GamePadController, GamePadControllerProto
from GamePadController import GamePadConnected

if on_raspberry_pi:
    from StepperController import StepperController
    from BeamerController import BeamerController
import Server
from Messages import GamePadSelectPressed
#from DataController import DataPool, PrintingTaskController
from DataBaseController import DataBaseController
from multiprocessing import Process




class SlaPrinterController(Observer):

    def __init__(self):

        print("Initalizing Controller")

        self.io_bus = MessageBus()
        self.io_bus.register(self)


        # ToDo: use this to broadcast a quit message to all started Processes from here
        # do I really need this ?
        #self.broadcast_bus = MessageBus()
        #self.broadcast_bus.register(self)


        if on_raspberry_pi:
            self.stepperController = StepperController(self.io_bus)

        self.pygameIoController = GamePadController(self.io_bus)



        self.data_bus = MessageBus()
        self.data_bus.register(self)
        self.db_controller = DataBaseController(in_memory_database, bus=self.data_bus)

        if on_raspberry_pi:
            self.pygameRenderController = BeamerController(bus=self.data_bus)

        self.server = Server.SlaPrinterApp(__name__, db_controller = self.db_controller, bus=self.data_bus)



    def start(self):



        # start msg buses
        self.io_bus.start()
        self.data_bus.start()


        self.pygameIoController.start()

        if on_raspberry_pi:
            self.pygameRenderController.start()
            #self.stepperController.start() -> currently not used as process

        self.server.run(host='0.0.0.0',debug=True, port=4242,  use_evalex=False, use_reloader=False)








    def release(self):

        #self.pygameIoController.stop
        print(self.pygameIoController)
        #self.pygameIoController.terminate()
        #self.pygameIoController.join()

        if on_raspberry_pi:
            self.pygameRenderController.stop()
            self.stepperController.stop()

        # stop msg buses
        print(self.io_bus)
        self.io_bus.stop()
        #self.io_bus.terminate()
        #self.io_bus.join()

        print(self.data_bus)
        self.data_bus.stop()
        #self.data_bus.terminate()
        #self.data_bus.join()

        # somehow stop server
        #self.server.stop()




    def notify(self, message):



        if isinstance(message, GamePadSelectPressed) or isinstance(message, QuitMessage):

            if isinstance(message.sender, GamePadControllerProto):
                print("[Controller] :: received message GamePadController >> " + message.msg)


            print("[Controller] :: received Quitmessage >> shutting down ...")

            self.release()


        # handle Data related Messages
        if isinstance(message.sender, DataBaseController):
            print("[Controller] :: received message from Database >> " + message.msg)

            if isinstance(message, NewPrintingTaskMsg):
                print("[Controller] :: .... >> received task >> " + str(message.task))

            print("")



        # handle IO messages
        if isinstance(message.sender, GamePadControllerProto):

            print("[Controller] :: received message GamePadController >> " + message.msg)

            if isinstance(message, GamePadConnected):
                print("[Controller] :: .... >> found controller >> " + str(message.sender))
            else:
                print("[Controller] :: " + str(message))

            print("")

