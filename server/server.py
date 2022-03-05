from flask import Flask, request, jsonify

import queryrequest
from fetcher_fascade import FetcherFascade
from queryrequest import QueryRequest
from dao.dal import DB
from flask_cors import CORS

from recommendation_response import recommendation_response_from_recommendation_result, RecommendationResponse
from recommendation_system.algorithm_impl.ziegler_nochols import ZieglerNichols
from recommendation_system.recommendation import Recommendation
from recommendation_types import RecommendationRequest, PID, RecommendationResult

app = Flask(__name__)
CORS(app)


class Server:
    def __init__(self, db=DB(), recommender=Recommendation(ZieglerNichols()), fetcher=FetcherFascade()):
        self.db: DB = db
        self.recommender: Recommendation = recommender
        self.fetcher: FetcherFascade = fetcher

    def query(self, query_request: QueryRequest) -> RecommendationResponse:
        self.db.create_request(query_request)
        recommendation_request = self.build_recommendation_request(query_request)
        result: RecommendationResult = self.recommender.recommend(recommendation_request)
        return recommendation_response_from_recommendation_result(result, recommendation_request.set_point)

    def query_endpoint(self):
        query_request = queryrequest.flask_request_to_request(request)
        result = self.query(query_request)
        return jsonify(result.__dict__)

    def build_recommendation_request(self, query_request: QueryRequest):
        p, i, d = self.fetcher.fetch_pid(query_request.pid_path)
        pid = PID(p, i, d)
        set_point = self.fetcher.fetch_set_point(query_request.set_point_path)
        current_sensor_value = self.fetcher.fetch_current_signal(query_request.value_path)
        convergence_time = query_request.simulation_seconds + (query_request.simulation_minutes * 60)
        simulation_data = self.db.get_samples_since(query_request.value_path)
        return RecommendationRequest(float(set_point),
                                     pid,
                                     int(convergence_time),
                                     simulation_data,
                                     float(current_sensor_value))


server = Server()


@app.route(rule='/', methods=('GET', 'POST'))
def act():
    return server.query_endpoint()


if __name__ == "__main__":
    app.run()
