__author__ = 'aslan'


from multiprocessing import Process
from Queue import Queue
import json
import requests as req

def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
        instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance


class Message(object):

    def __init__(self, path, data):
        self.path = path
        self.data = data

@singleton
class ServerConnection(Process):

    message_stack = Queue()

    def __init__(self, url):
        Process.__init__(self)
        self.__url = "http://http://192.168.178.28/"

    def run(self):

        while True:

            if not self.message_stack.empty():

                # get message object from FIFO message stack
                msg = self.message_stack.get()

                # json encode data
                data = json.dumps({"dat": msg.data})

                # send data to url + path
                target = str(self.__url + msg.path)
                r = req.post(target, data)



    def post_msg(self, message):

        if isinstance(message, Message):
            self.message_stack.put(message)