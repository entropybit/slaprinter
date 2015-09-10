__author__ = 'mithrawnuruodo'


from multiprocessing import Process, Queue
from abc import ABCMeta, abstractmethod

class Message(object):

    __metaclass__ = ABCMeta

    def __init__(self, sender, description):
        self.sender = sender
        self.description = description

class Observer(object):

    __metaclass__ = ABCMeta

    def __init__(self, bus):
        bus.register(self)

    @abstractmethod
    def notify(self,Message):
        pass


class Observable(object):

    bus = None

    def __init__(self, bus):
        self.__bus = bus

    def put_message(self,message):
        self.__bus.put(message)

class MessageBus(Process):


    def __init__(self):
        self.running = False
        Process.__init__(self)
        self.msg_que = Queue()
        self.observers = []

    def start(self):
        self.running = True
        Process.start(self)


    def stop(self):
        self.running = False
        Process.join(self)

    def register(self, observer):

        if isinstance(observer, Observer):
            self.observers.append(observer)

    def put(self, msg):
        self.msg_que.put(msg)


    def run(self):

        while self.running:

            i =0
            while not self.msg_que.empty():


                msg = self.msg_que.get()

                #print("ith element [" + str(i) +" from msg stack " + str(msg))

                #j = 0
                for obs in self.observers:

                    #print("jth observer [" + str(j) + " | " + str(obs) + " notified")
                    obs.notify(msg)
                    #j = j +1

                #i = i +1




import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Worker(Process, Observable):

    def __init__(self, bus):

        Observable.__init__(self, bus=bus)
        Process.__init__(self)
        self.running = False



    def start(self):

        self.running = True
        Process.start(self)

    def stop(self):

        self.running = False
        Process.join(self)

    def run(self):
        import numpy as np
        np.random.seed(42)
        import time
        while self.running:


            t = np.random.rand()

            text = id_generator(20)
            self.put_message(text)

            time.sleep(t)


class PrintingObserver(Observer):


    def notify(self,Message):

        print("received msg: " + str(Message))


class Runner(Process):

    def __init__(self):
        self.running = False
        Process.__init__(self)

    def start(self):
        self.running = True
        Process.start(self)

    def stop(self):
        self.running = False
        Process.join()

    def run(self):

        bus = MessageBus()

        obs = PrintingObserver(bus=bus)
        worker = Worker(bus=bus)

        t = 10

        bus.start()
        worker.start()
        time.sleep(t)


        worker.stop()
        bus.stop()

        print("stopped after " + str(t) +"s")



import time

if __name__=="__main__":


    run = Runner()
    run.start()








