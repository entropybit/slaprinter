__author__ = 'mithrawnuruodo'


from Config import in_memory_database,log_controller_input

from MessageHandler import MessageBus, Observer
from Messages import NewPrintingTaskMsg, QuitMessage
from PygameController import PygameController, PygameControllerProto
from Messages import GamePadConnected, GamePadShoulderLPressed, GamePadShoulderRPressed
from Messages import GamePadAPressed, DataReceivedMessage
from StepperController import StepperController
import Server
from Messages import GamePadSelectPressed
#from DataController import DataPool, PrintingTaskController
from DataBaseController import DataBaseController
from multiprocessing import Process

from ServiceFunctions import now
import sys







class SlaPrinterController(Observer):

    def __init__(self):

        print("Controller initializing")

        self.io_bus = MessageBus()
        self.io_bus.register(self)


        # ToDo: use this to broadcast a quit message to all started Processes from here
        # do I really need this ?
        #self.broadcast_bus = MessageBus()
        #self.broadcast_bus.register(self)

        self.stepperController = StepperController(bus=self.io_bus)

        self.data_bus = MessageBus()
        self.data_bus.register(self)
        #if mode != "stepper_calibration":
        self.db_controller = DataBaseController(in_memory_database, bus=self.data_bus)

        self.pygameIoController = PygameController(sending_bus=self.io_bus, receiving_bus=self.data_bus)

        #self.pygameRenderController = BeamerController(bus=self.data_bus)


        #if mode != "stepper_calibration":
        self.server = Server.SlaPrinterApp(__name__, db_controller = self.db_controller, bus=self.data_bus)

        #server_func = lambda: self.server.run(host='0.0.0.0',debug=True, port=4242,  use_evalex=False, use_reloader=False)
        #self.server_p = Process(target=server_func)


    def start(self):

        self.server.start()

        # start msg buses
        self.io_bus.start()
        self.data_bus.start()
        self.pygameIoController.start()
        self.stepperController.start()

        #self.server.run(host='0.0.0.0',debug=True, port=4242,  use_evalex=False, use_reloader=False)

        #self.server_p.start()



    def stop(self):


        self.stepperController.stop()
        self.pygameIoController.stop()
        self.data_bus.stop()
        self.io_bus.stop()

        self.server.stop()

        #sys.exit(0)
        #self.server_p.terminate()
        #self.server_p.join()



    def notify(self, message):



        if isinstance(message, GamePadSelectPressed) or isinstance(message, QuitMessage):

            if isinstance(message.sender, PygameControllerProto):
                if log_controller_input:
                    print("[" + str(now()) + "] Controller :: received message GamePadController >> " + message.msg)


            if log_controller_input:
                print("[" + str(now()) + "] Controller :: received Quitmessage >> shutting down ...")

            self.stop()


        # handle Data related Messages
        if isinstance(message.sender, DataBaseController):

            if log_controller_input:
                print("[" + str(now()) + "] Controller :: received message from Database >> " + message.msg)

            if isinstance(message, NewPrintingTaskMsg):
                if log_controller_input:
                    print("[" + str(now()) + "] Controller :: .... >> received task >> " + str(message.task))




        # handle IO messages
        if isinstance(message.sender, PygameControllerProto):


            if log_controller_input:
                print("[" + str(now()) + "] Controller :: received message GamePadController >> " + message.msg)

            if isinstance(message, GamePadConnected):

                if log_controller_input:
                    print("[" + str(now()) + "] Controller :: .... >> found controller >> " + str(message.sender))

            if isinstance(message, GamePadAPressed):
                msg = DataReceivedMessage(None, "bla")
                self.data_bus.put(msg)
            else:
                if log_controller_input:
                    print("[" + str(now()) + "] Controller :: " + str(message))


