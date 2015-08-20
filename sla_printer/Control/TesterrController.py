__author__ = 'mithrawnuruodo'

from MessageHandler import Observer
from threading import Thread

class BeamerController(Observer, Thread):

    def __init__(self, dispatcher):

        self.dispatcher = dispatcher
        self.dispatcher.register_observer(self)
        self.running = True

        print("beamer controller created")

        Thread.__init__(self)

    def notify(self,Message):
        print("[beamer]: " + str(Message.msg))


    def stop(self):
        self.running = False

    def start(self):

        self.running = True
        Thread.start(self)


    def run(self):

        while self.running:
            pass