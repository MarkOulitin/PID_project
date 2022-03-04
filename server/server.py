from flask import Flask, request, jsonify

import queryrequest
import simulator_mock
from dao.dal import DB
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


class Server:
    def __init__(self, db=DB(), simulator=simulator_mock.Simulator()):
        self.db = db
        self.simulator = simulator

    def query(self, query_request):
        self.db.create_request(query_request)
        result = self.simulator.simulate(query_request)
        return result

    def query_endpoint(self):
        query_request = queryrequest.flask_request_to_request(request)
        result = self.query(query_request)
        return jsonify(result.__dict__)


server = Server()


@app.route(rule='/', methods=('GET', 'POST'))
def act():
    return server.query_endpoint()


if __name__ == "__main__":
    app.run()
