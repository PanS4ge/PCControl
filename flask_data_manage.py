# create a flask app to manage data with json

import os
import json
import flask
import flask_cors
import specs
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# create a flask app
app = flask.Flask(__name__)
flask_cors.CORS(app)

def get_endpoint():
    return "http://localhost:8081"

# create a route to get data
@app.route('/data')
def get_data():
    return json.dumps(specs.get_specs())

def run():
    #print(get_endpoint())
    # get path to current directory
    path = os.path.dirname(os.path.realpath(__file__))
    try:
        with open(f"{path}/tempconfig.json", "r") as f:
            data = json.loads(f.read())
            with open(f"{path}/tempconfig.json", "w") as fw:
                data['endpoint'] = get_endpoint()
                fw.write(json.dumps(data))
    except Exception:
        with open(f"{path}/tempconfig.json", "w") as f:
            data = json.loads("{}")
            data['endpoint'] = get_endpoint()
            f.write(json.dumps(data))
    app.run(host='0.0.0.0', port=8081)
    os.system("cls")

def stop():
    exit(0)