__author__ = 'aslan'

import json
from flask import Flask
from flask import render_template
from flask import request
from Model import RawData

import json
from threading import Thread
import Control as cntrl



app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():

    data = cntrl.DataPool()

    return render_template("index.html", packages = data.get_data())


@app.route("/post/raw/",  methods = ['POST'])
def post_data():


    data = json.loads(request.data)
    print("[received raw adata]: " + str(data))

    data_pool = cntrl.DataPool()


    if "data" in data:
        d  = RawData(data["data"])
        data_pool.add(d)
        return str(d)
    else:
        return "no data received"


@app.route("/input/<pid>",  methods = ['POST','GET'])
def echo_string_with_id(pid):

    data = json.loads(request.data)
    print(data)

    if "text" in data:
        text  = data["text"]
        return text
    else:
        return "bla"

    #if request.headers['Content-Type'] == 'text/plain':
    #    return "Text Message: " + request.data

    #elif request.headers['Content-Type'] == 'application/json':
    #    return "JSON Message: " + json.dumps(request.json)
    #elif request.headers['Content-Type'] == 'application/octet-stream':
    #    f = open('./binary', 'wb')
    #    f.write(request.data)
    #    f.close()
    #    return "Binary message written!"

    #else:
    #    return "415 Unsupported Media Type ;)"



@app.errorhandler(404)
def page_not_found(e):
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

def start_flask():
    app.run(host='0.0.0.0',debug=True, port=4242,  use_evalex=False)



