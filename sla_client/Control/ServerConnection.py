__author__ = 'aslan'


from multiprocessing import Process, Queue
#from Queue import Queue
import json
import requests as req
from Model import SerializablePackage
import time
import traceback

def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
        instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance




@singleton
class ServerConnection(Process):



    def __init__(self, url, send_interval=0.01):
        Process.__init__(self)
        self.__package_stack = Queue()
        self.__url = url
        self.__send_interval = send_interval
        self.__running = True

    def run(self):

        while self.__running:

            if not self.__package_stack.empty():


                # get message object from FIFO message stack
                data = self.__package_stack.get()

                try:
                    target = str(self.__url + data.path)
                    data = data.json()
                    # send data to url + path
                    r = req.post(target, data)
                    print("data send")
                    print(r.text)
                except:
                    #print("tried to serialize non data package")
                    traceback.print_exc()




            time.sleep(self.__send_interval)


    def post_data(self, data):

        print("post_data call")
        self.__package_stack.put(data)
        print(data.__hash__())




    def start(self):

        print("starting server connection")
        self.__running = True

        Process.start(self)

    def stop(self):
        self.__running = False
        self.terminate()
        self.join()