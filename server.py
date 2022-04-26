from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import FileStorage

import queryrequest
from dao.dal import DB
from queryrequest import QueryRequest
from recommendation_response import recommendation_response_from_recommendation_result, RecommendationResponse
from recommendation_system.algorithm_impl.ziegler_nichols import ZieglerNichols
from recommendation_system.recommendation import Recommendation
from recommendation_types import RecommendationRequest, PID, RecommendationResult, simulation_data_from_file

app = Flask(__name__)
CORS(app)


class Server:
    def __init__(self, db=DB(True), recommender=Recommendation(ZieglerNichols())):
        self.db: DB = db
        self.recommender: Recommendation = recommender

    def query(self, query_request: QueryRequest, file: FileStorage) -> RecommendationResponse:
        # self.db.create_request(query_request)
        recommendation_request = self.build_recommendation_request(query_request, file)
        result: RecommendationResult = self.recommender.recommend(recommendation_request)
        return recommendation_response_from_recommendation_result(result, recommendation_request.set_point)

    def query_endpoint(self):
        query_request = queryrequest.flask_request_to_request(request)
        file = request.files['file']
        result = self.query(query_request, file)
        ret = jsonify(result.__dict__)
        return ret

    def build_recommendation_request(self, query_request: QueryRequest, file: FileStorage):
        pid = PID(query_request.p, query_request.i, query_request.d)
        set_point = 0  # todo
        convergence_time = query_request.simulation_seconds + (query_request.simulation_minutes * 60)
        simulation_data = simulation_data_from_file(file)
        return RecommendationRequest(set_point, pid, int(convergence_time), simulation_data)


server = Server()


@app.route(rule='/', methods=('GET', 'POST'))
@cross_origin()
def act():
    return server.query_endpoint()


if __name__ == "__main__":
    app.run()
