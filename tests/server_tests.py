import unittest
from numbers import Number
from random import randint
from typing import List

import numpy as np

from queryrequest import QueryRequest
from recommendation_response import RecommendationResponse
from recommendation_types import PID, RecommendationRequest, RecommendationResult, PidDataPoints
from sample import Sample
from server import Server
from tests.resources.mocks.db_mock import DbMock
from tests.resources.mocks.fetcher_mock import FetcherMock
from tests.resources.mocks.recommender_mock import RecommenderMock


class TestServer(unittest.TestCase):
    def test_query(self):
        db = DbMock()
        recommender = RecommenderMock()
        fetcher = FetcherMock()
        server = Server(db=db, recommender=recommender, fetcher=fetcher)

        seconds_back = 24 * 60 * 60
        set_point = float(randint(0, 100))
        pid = PID(float(randint(0, 100)), float(randint(0, 100)), float(randint(0, 100)))
        value = float(randint(0, 100))
        samples = sample_of_gaussian(pid, set_point)
        request = QueryRequest()
        response = random_recommendation_result()
        rec_request = recommendation_request(set_point, pid, request.simulation_seconds + (request.simulation_minutes * 60), samples, value)

        fetcher.set_ret_values(request.pid_path, pid, request.set_point_path, set_point, request.value_path, value)
        db.set_expected_values(request.value_path, seconds_back, samples)
        recommender.set_expected_values(rec_request, response)

        assert server.query(request).__eq__(RecommendationResponse(
            response.old_pid.p,
            response.old_pid.i,
            response.old_pid.d,
            response.recommended_pid.p,
            response.recommended_pid.i,
            response.recommended_pid.d,
            set_point,
            [(response.old_pid_data_points.time, response.old_pid_data_points.amplitude)],
            [(response.recommended_pid_data_points.time, response.recommended_pid_data_points.amplitude)]
        ))


def sample_of_gaussian(pid: PID, set_point: Number):
    acc = []
    a = lambda x: np.exp(-np.power(x - 1, 2.) / (2 * np.power(200, 2.)))
    for x in range(1000):
        acc.append(Sample(1, 2, a(x - 500) * 200, 4.0, set_point, 90182573 + x, pid))
    return acc


def recommendation_request(set_point: Number,
                           pid: PID,
                           convergence_time: Number,
                           simulation_data: List[Sample],
                           current_sensor_value: Number):
    return RecommendationRequest(set_point, pid, convergence_time,
                                 list(map(lambda s: s.to_simulation_data(), simulation_data)))


def random_recommendation_result():
    return RecommendationResult(
        PID(float(randint(0, 100)), float(randint(0, 100)), float(randint(0, 100))),
        PidDataPoints([(randint(1, 2))], [(randint(1, 2))]),
        PID(float(randint(0, 100)), float(randint(0, 100)), float(randint(0, 100))),
        PidDataPoints([(randint(1, 2))], [(randint(1, 2))])
    )
