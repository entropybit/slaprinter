__author__ = 'aslan'

import json
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import Response

from Model import PrintingTaskData
from Control.ServiceFunctions import now
from multiprocessing import Event, Process
import base64
import time

#import sys
#import os
# set sytem path to be directory above so that a can be a
# package namespace
#DIRECTORY_SCRIPT = os.path.dirname(os.path.realpath(__file__))
#sys.path.insert(0,DIRECTORY_SCRIPT+"/..")

from Control.MessageHandler import Observable, Observer
from Control.Messages import QuitMessage

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__)) + "/Server"
TEMPLATE_DIR = PROJECT_DIR + '/templates'
STATIC_DIR = PROJECT_DIR +'/static'
#print("PROJECT_DIR : "+str(PROJECT_DIR))
#print("STATIC_DIR : "+str(STATIC_DIR))
#print("TEMPLATE_DIR :"+str(TEMPLATE_DIR))
#import Control as cntrl



class RoutingData(object):
    def __init__(self, args, kwargs):
        super(RoutingData, self).__init__()
        self.args = args
        self.kwargs = kwargs

def route(*args, **kwargs):
    def wrap(fn):
        l = getattr(fn, '_routing_data', [])
        l.append(RoutingData(args, kwargs))
        fn._routing_data = l
        return fn
    return wrap

class SlaPrinterAppProto(object):
    pass

class SlaPrinterApp(Flask, Observable, Observer, Process):
    def __init__(self, import_name, db_controller = None, bus = None):
        #super(SlaPrinterApp, self).__init__(import_name, template_folder=TEMPLATE_DIR, static_url_path=STATIC_DIR)
        Flask.__init__(self,import_name, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)
        Observable.__init__(self, bus)
        Observer.__init__(self, bus)
        Process.__init__(self)
        self.exit = Event()


        self.endpoint_prefix = None
        for name in dir(self):
            if hasattr(getattr(self, name), ("_routing_data")):
                fn = getattr(self, name)
                rds = fn._routing_data
                for rd in rds:
                    self.route(*rd.args, **rd.kwargs)(fn)


        self.register_error_handler(404, self.page_not_found)
        self.db_controller = db_controller

        print("Flask Server initializing")

        #func = lambda: self.run(host='0.0.0.0',debug=True, port=4242,  use_evalex=False, use_reloader=False)
        #self.runner_process = Process(target=func)


    @route("/")
    @route("/index")
    def index(self):

        if self.db_controller is not None:
            tasks = self.db_controller.printing_tasks()
            print("tasks: " + str(tasks))
            active_job = self.db_controller.active_job()
            return render_template("index.html", printing_tasks = tasks, active_job= active_job)

        else:
            return render_template("index.html")

    @route("/enqueue")
    def enqueue(self):

        return render_template("enqueue.html")

    @route("/info")
    def info(self):

        return render_template("info.html")

    @route("/quit", methods = ['POST', 'GET'])
    def quit(self):


        msg = QuitMessage(SlaPrinterAppProto(),"sla printer shutting down")
        self.put_message(msg)

        return "quitting"

    @route("/post/raw/", methods = ['POST'])
    def post_data(self):
        '''
        function used to send simple raw string data to 3D printer

        :return: according success / fail message
        '''


        # get current data pool to store new objects
        #data_pool = cntrl.DataPool()

        # load data
        data = json.loads(request.data)


        # if "data" in data:
        #     d  = RawData(data["data"])
        #     data_pool.add(d)
        #     return str(d)
        # else:
        #     return "no data received"

    @route("/post/task/",  methods = ['POST'])
    def post_task(self):
        '''
        Function used to send printing task to 3D printer

        :return: according success / fail message
        '''

        # load data
        data = json.loads(request.data)

        # create empty printing task
        task = PrintingTaskData()

        # if received data parseable to task object store new printing task
        if task.parse(data):

            if self.db_controller is not None:
                jid = self.db_controller.save_printing_task(task)
                return json.dumps({"id": jid})
            else:
                return "no valid printing task received"
        else:
            return "invalid data"


    @route("/download/<jid>/",  methods = ['POST', 'GET'])
    def download_zip(self, jid):

        # data_pool = cntrl.DataPool()
        #
        #
        task = self.db_controller.get_by_id(jid)

        if task is not None:

            zip = task.stl_file
            zip = base64.decodestring(zip)
            filename = task.file_name

        else:
            zip = ''
            filename = ''


        return Response(zip,
                mimetype='application/zip',
                headers={'Content-Disposition':'attachment;filename=' + str(filename) + '.zip'})
                #headers={'Content-Disposition':'attachment;filename=' + str(file_name) + '.zip'})

    @route("/stepper/down/<steps>/",  methods = ['POST', 'GET'])
    def steps_down(self, steps):
        print(" received " + str(steps) + " down message")


    def page_not_found(self, e):
        return render_template('404.html'), 404


    def notify(self, msg):
        print("[" + str(now()) + "] Server :: " + str(msg))



    def start(self):
        print("[" + str(now()) + "] Server :: starting ")
        #self.runner_process.start()
        #self.running = True
        Process.start(self)



    def stop(self):
        self.exit.set()
        self.terminate()
        #self.join()

    def run(self):

        # run server
        Flask.run(self, host='0.0.0.0',debug=True, port=4242,  use_evalex=False, use_reloader=False)


        while not self.exit.is_set():

            print("[" + str(now()) + "] server heartbeat ")
            time.sleep(0.5)


        print("[" + str(now()) + "] server shutting down ")

        return





if __name__ == "__main__":

    server =SlaPrinterApp(__name__)
    server.run(host='0.0.0.0',debug=True, port=4242,  use_evalex=False)