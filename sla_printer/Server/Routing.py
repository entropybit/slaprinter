__author__ = 'aslan'

import json
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import Response

from Model import PrintingTaskData

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

class SlaPrinterApp(Flask):
    def __init__(self, import_name, db_controller = None):
        #super(SlaPrinterApp, self).__init__(import_name, template_folder=TEMPLATE_DIR, static_url_path=STATIC_DIR)
        super(SlaPrinterApp, self).__init__(import_name, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)

        self.endpoint_prefix = None
        for name in dir(self):
            if hasattr(getattr(self, name), ("_routing_data")):
                fn = getattr(self, name)
                rds = fn._routing_data
                for rd in rds:
                    self.route(*rd.args, **rd.kwargs)(fn)


        self.register_error_handler(404, self.page_not_found)
        self.db_controller = db_controller


    @route("/")
    @route("/index")
    def index(self):

        #data = cntrl.PrintingTaskController()

        if self.db_controller is not None:
            tasks = self.db_controller.printing_tasks()
            active_job = self.db_controller.active_job()
            return render_template("index.html", printing_tasks = tasks, active_job= active_job)

        else:
            return render_template("index.html")

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


    @route("/download/<tid>/",  methods = ['POST', 'GET'])
    def download_zip(self, tid):

        # data_pool = cntrl.DataPool()
        #
        #
        # task = data_pool.get_by_id(tid)
        #
        # if task is not None:
        #
        #     zip = task.stl_file
        #     zip = base64.decodestring(zip)
        #
        # else:
        zip = ''

        file_name = "bla"

        return Response(zip,
                mimetype='application/zip',
                #headers={'Content-Disposition':'attachment;filename=' + str(task.file_name) + '.zip'})
                headers={'Content-Disposition':'attachment;filename=' + str(file_name) + '.zip'})


    def page_not_found(self, e):
        return render_template('404.html'), 404


#if __name__ == "__main__":
#    app.run(host='0.0.0.0',debug=True, port=4242)

#class StartFlask(Thread):
#
#    def __init__(self, dispatcher):
#        Thread.__init__(self)
#        self.__dispatcher = dispatcher
#
#    def run(self):

#def start_flask():
#    app.run(host='0.0.0.0',debug=True, port=4242,  use_evalex=False)



if __name__ == "__main__":

    server =SlaPrinterApp(__name__)
    server.run(host='0.0.0.0',debug=True, port=4242,  use_evalex=False)