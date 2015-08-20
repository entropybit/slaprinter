__author__ = 'mithrawnuruodo'


__author__ = 'mithrawnuruodo'

from threading import Thread
from time import sleep
from Queue import Queue
from abc import ABCMeta, abstractmethod

class Observer(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self,Message):
        pass


class Observable(object):


    def __init__(self, dispatcher):
        self.__dispatcher = dispatcher


    def put_message(self,message):
        self.__dispatcher.put_message(message)




class Dispatcher(Thread):

    def __init__(self, *args, **kwargs):
        """

        Init the Dispatcher object by defining a lisf of interested threads and a message stack
        where latter is realized by a Queue.
        Thus, messages are put at the top and taken from the bottom which is suitable for a
        secure communication between several threads.
        The objects from the queue package also seem to have the property of being thread secure.
        Since the Dispatcher is also derived from Thread it runs in parallel with the other threaded
        objects.

        """
        super(Dispatcher, self).__init__(*args, **kwargs)
        self.__interested_threads = []
        self.__message_stack = Queue()
        self.running = True

    def run(self):
        """
        For all eternity look if there is still a message on the message stack. If so dispatch it, else
        sleep for a short while

        """
        while self.running:
            while not self.__message_stack.empty():
                msg = self.__message_stack.get()
                self.dispatch_message(msg)
            #else:
            #    sleep(0.1)

    def register_observer(self, thread):
        """

        :param thread: A thread which needs to synchronize with the sending thread of this dispatcher.
                       By registering it ot the list of interested threads it will receive each message
                       send by the sending object. Thus, a synchronization between the objects is achieved.

        """
        self.__interested_threads.append(thread)


    def put_message(self,message):
        """
        The put message function is used by the sending object to send a message.
        Effectively a message is send by putting it to the top of the message stack, the actual sending or
        dispatching will be done in the run function so within the thread of the Dispatcher.
        While the call to put_message happens from within the Thread of the sending object.

        :param message: message which is to be send to observers

        """
        self.__message_stack.put(message)



    def dispatch_message(self, message):
        """
        This function is used within run to actually send / dispatch a specific message to all interested threads.

        :param message: message which is to be send
        :return:
        """
        for thread in self.__interested_threads:
            thread.notify(message)

    def stop(self):
        self.running = False



    def start(self):

        self.running = True
        Thread.start(self)


