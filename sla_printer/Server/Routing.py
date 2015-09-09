__author__ = 'aslan'

import json
from flask import Flask
from flask import render_template
from flask import request
from flask import Response
#from Model import RawData, PrintingTaskData
import base64

import json
from threading import Thread
import Control as cntrl

class SlaPrinterApp(Flask):
    def __init__(self, import_name):
        super(SlaPrinterApp, self).__init__(import_name)


    def index(self):

        data = cntrl.PrintingTaskController()


        return render_template("index.html", printing_tasks = data.printing_tasks, active_job= data.active_job())


    @app.route("/post/raw/",  methods = ['POST'])
    def post_data(self):
        '''
        function used to send simple raw string data to 3D printer

        :return: according success / fail message
        '''


        # get current data pool to store new objects
        data_pool = cntrl.DataPool()

        # load data
        data = json.loads(request.data)


        if "data" in data:
            d  = RawData(data["data"])
            data_pool.add(d)
            return str(d)
        else:
            return "no data received"

    @app.route("/post/task/",  methods = ['POST'])
    def post_task(self):
        '''
        Function used to send printing task to 3D printer

        :return: according success / fail message
        '''


        # get current data pool to store new objects
        data_pool = cntrl.DataPool()

        # load data
        data = json.loads(request.data)

        # create empty printing task
        task = PrintingTaskData()

        # if received data parseable to task object store new printing task
        if task.parse(data):
            #print(task)
            data_pool.add(task)
            return "printing task received"
        else:
            return "no valid printing task received"

    @app.route("/download/<tid>/",  methods = ['POST', 'GET'])
    def download_zip(self, tid):

        data_pool = cntrl.DataPool()


        task = data_pool.get_by_id(tid)

        if task is not None:

            zip = task.stl_file
            zip = base64.decodestring(zip)

        else:
            zip = ''

        return Response(zip,
                mimetype='application/zip',
                headers={'Content-Disposition':'attachment;filename=' + str(task.file_name) + '.zip'})



    @app.errorhandler(404)
    def page_not_found(self, e):
        return render_template('404.html'), 404



        #self.route("/hello")(self.hello)


#app = Flask(__name__)

@app.route('/')
@app.route('/index')

#if __name__ == "__main__":
#    app.run(host='0.0.0.0',debug=True, port=4242)

#class StartFlask(Thread):
#
#    def __init__(self, dispatcher):
#        Thread.__init__(self)
#        self.__dispatcher = dispatcher
#
#    def run(self):

def start_flask():
    app.run(host='0.0.0.0',debug=True, port=4242,  use_evalex=False)



