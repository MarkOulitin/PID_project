import unittest
from numbers import Number
import random
from random import randint
from typing import List
from string import ascii_lowercase as letters

from werkzeug.datastructures import FileStorage

from queryrequest import QueryRequest
from recommendation_system.types.recommendation_response import RecommendationResponse
from recommendation_system.types.recommendation_types import PID, RecommendationRequest, RecommendationResult, PidDataPoints, SimulationData, \
    simulation_data_from_file
from server import Server
from tests.resources.mocks.db_mock import DbMock
from tests.resources.mocks.recommender_mock import RecommenderMock


class TestServer(unittest.TestCase):
    def test_query(self):
        with open('resources/data/test1.csv', 'rb') as fp:
            file = FileStorage(fp)
            simulation_data = simulation_data_from_file(file)
            db = DbMock()
            recommender = RecommenderMock()

            server = Server(db=db, recommender=recommender)
            seconds_back = 24 * 60 * 60 * randint(0, 100)
            plc_path = random_string()
            set_point = float(randint(0, 100))
            pid = PID(float(randint(0, 100)), float(randint(0, 100)), float(randint(0, 100)))
            response = random_recommendation_result()
            request = generate_query_request(plc_path, pid, seconds_back, set_point)
            rec_request = recommendation_request(set_point, pid, seconds_back, simulation_data)

            recommender.set_expected_values(rec_request, response)

        with open('resources/data/test1.csv', 'rb') as fp:
            file = FileStorage(fp)
            query = server.query(request, file)
            correct = RecommendationResponse(
                    response.old_pid.p,
                    response.old_pid.i,
                    response.old_pid.d,
                    response.recommended_pid.p,
                    response.recommended_pid.i,
                    response.recommended_pid.d,
                    set_point,
                    [(response.old_pid_data_points.time[0], response.old_pid_data_points.amplitude[0])],
                    [(response.recommended_pid_data_points.time[0], response.recommended_pid_data_points.amplitude[0])])

            incorrect = RecommendationResponse(
                    response.old_pid.p + 1,
                    response.old_pid.i,
                    response.old_pid.d,
                    response.recommended_pid.p,
                    response.recommended_pid.i,
                    response.recommended_pid.d,
                    set_point,
                    [(response.old_pid_data_points.time[0], response.old_pid_data_points.amplitude[0])],
                    [(response.recommended_pid_data_points.time[0], response.recommended_pid_data_points.amplitude[0])])

            self.assertEqual(query, correct)
            self.assertNotEqual(query, incorrect)


def generate_query_request(plc_path, pid, simulation_duration, set_point) -> QueryRequest:
    return QueryRequest(plc_path, pid.p, pid.i, pid.d, simulation_duration / 60, simulation_duration % 60, set_point)


def recommendation_request(set_point: Number,
                           pid: PID,
                           convergence_time: Number,
                           simulation_data: List[SimulationData]):
    return RecommendationRequest(set_point, pid, convergence_time, simulation_data)


def random_recommendation_result():
    return RecommendationResult(
        PID(float(randint(0, 100)), float(randint(0, 100)), float(randint(0, 100))),
        PidDataPoints([(randint(1, 2))], [(randint(1, 2))]),
        PID(float(randint(0, 100)), float(randint(0, 100)), float(randint(0, 100))),
        PidDataPoints([(randint(1, 2))], [(randint(1, 2))])
    )


def random_string():
    return ''.join(random.choice(letters) for i in range(10))

