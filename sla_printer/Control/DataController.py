__author__ = 'mithrawnuruodo'


from threading import Thread
from MessageHandler import Observable, Dispatcher
import Control
import Model

class DataPool(Thread, Observable):

    pool = set()

    def __init__(self, dispatcher=Dispatcher()):

        Thread.__init__(self)
        Observable.__init__(self, dispatcher)



    def add(self, data):

        if isinstance(data, Model.Data):
            self.pool.add(data)
            self.put_message(Control.Messages.DataReceivedMessage(self, data))
            return True

        return False


    def remove(self, data):

        if isinstance(data, Model.data):
            self.pool.remove(data)
            self.put_message(Control.Messages.DataDeletedMessage(self, data))
            return True

        return False

    def get_data(self):
        return [str(d) for d in list(self.pool)]






