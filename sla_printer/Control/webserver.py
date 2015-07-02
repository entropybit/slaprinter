__author__ = 'aslan'

import json
from flask import Flask
app = Flask(__name__)

@app.route("/home/pi/druckerskripte/input/<pid>")
def echo_string_with_id():
    data = json.loads(request.data)
    text = data["text"]
    return text

if __name__ == "__main__":
    app.run(host='0.0.0.0')