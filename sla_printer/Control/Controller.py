__author__ = 'mithrawnuruodo'

from MessageHandler import Dispatcher
from GamePadController import SnesController
from Server import start_flask


class SlaPrinterController(object):

    def __init__(self):

        self.dispatcher = Dispatcher()
        self.gamePadController = SnesController(self.dispatcher)


    def start(self):

        self.gamePadController.start()
        #start_flask()
