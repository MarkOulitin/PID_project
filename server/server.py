from flask import Flask, request, jsonify

import queryrequest
import simulator_mock
from dao.dal import DB

app = Flask(__name__)
db = DB()
simulator = simulator_mock.Simulator()


@app.route(rule='/', methods=('GET', 'POST'))
def query():
    flask_request_to_request = queryrequest.flask_request_to_request(request)
    # db.create_request(flask_request_to_request)
    result = simulator.simulate(flask_request_to_request)
    return jsonify(result.__dict__)


app.run()
