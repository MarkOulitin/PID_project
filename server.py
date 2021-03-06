import os

import werkzeug.exceptions
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

import queryrequest
from constants import DEFAULT_ALGORITHM, TEST
from dao.dal import DB
from queryrequest import QueryRequest
from recommendation_system.algorithm_impl.custom_algorithm import CustomAlgorithm
from recommendation_system.types.recommendation_response import recommendation_response_from_recommendation_result, \
    RecommendationResponse, default_recommendation_response
from recommendation_system.algorithm_impl.ziegler_nichols import ZieglerNichols
from recommendation_system.recommendation import Recommendation
from recommendation_system.types.recommendation_types import RecommendationRequest, PID, RecommendationResult, \
    simulation_data_from_file

app = Flask(__name__)
CORS(app)


class Server:
    def __init__(self, db=DB(True), recommender=Recommendation(ZieglerNichols())):
        self.db: DB = db
        self.recommender: Recommendation = recommender
        self.uploads_dir = os.path.join(app.instance_path, 'uploads')

    def query_endpoint(self):
        algorithm_file_name = server.upload_algorithm_endpoint()
        query_request, algorithm_name = queryrequest.flask_request_to_request(
            request)
        if algorithm_file_name:
            algorithm_name = algorithm_file_name
        file = request.files['file']
        result = self.query(query_request, file, algorithm_name)
        ret = jsonify(result.__dict__)
        return ret

    def query(self, query_request: QueryRequest, file: FileStorage, algorithm_name: str) -> RecommendationResponse:
        self.db.insert_query_request(query_request)
        recommendation_request = self.build_recommendation_request(
            query_request, file)
        if query_request.plc_path == TEST:
            return default_recommendation_response(query_request.p, query_request.i, query_request.d,
                                                   query_request.set_point,
                                                   recommendation_request.simulation_data)
        recommender = \
            self.recommender if algorithm_name == DEFAULT_ALGORITHM else Recommendation(CustomAlgorithm(algorithm_name))
        recommender.recommend(recommendation_request)
        return recommendation_response_from_recommendation_result(result, recommendation_request.set_point)

    def build_recommendation_request(self, query_request: QueryRequest, file: FileStorage):
        pid = PID(query_request.p, query_request.i, query_request.d)
        set_point = query_request.set_point
        convergence_time = query_request.simulation_seconds + \
                           (query_request.simulation_minutes * 60)
        simulation_data = simulation_data_from_file(file, query_request)
        return RecommendationRequest(set_point, pid, int(convergence_time), simulation_data)

    def upload_algorithm_endpoint(self):
        try:
            file = request.files['algorithmFile']
            return self.upload_algorithm(file)
        except:
            return None

    def upload_algorithm(self, file: FileStorage, prefix=None):
        if prefix is None:
            prefix = self.uploads_dir
        if not file.filename.endswith('.py'):
            raise Exception
        os.makedirs(prefix, exist_ok=True)
        file.save(os.path.join(prefix, secure_filename(file.filename)))
        return file.filename

    def get_algorithms_endpoint(self):
        ret = self.get_algorithms()
        return jsonify({'result': ret})

    def get_algorithms(self, prefix=None):
        if prefix is None:
            prefix = self.uploads_dir
        ret = [DEFAULT_ALGORITHM]
        os.makedirs(prefix, exist_ok=True)
        for file in os.listdir(prefix):
            if file.endswith(".py"):
                ret.append(file)
        return ret


server = Server()


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_exception(e):
    return str(e), 500


@app.route(rule='/', methods=('GET', 'POST'))
@cross_origin()
def act():
    return server.query_endpoint()


@app.route(rule='/algorithm', methods=('GET', 'POST'))
@cross_origin()
def algo():
    return server.get_algorithms_endpoint() if request.method == 'GET' else None


if __name__ == "__main__":
    app.register_error_handler(Exception, handle_exception)
    app.run()
