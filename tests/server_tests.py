import unittest
import uuid
from unittest import mock
from unittest.mock import patch, Mock

from dao.dal import DB
from queryrequest import QueryRequest
from server.server import Server
from simulator_mock import Simulator
from simulator_response import SimulatorResponse


class MockDB(DB):
    def create_request(self, request):
        pass


class MockSimulator(Simulator):
    def __init__(self):
        self.ret_value = None

    def set_return_value(self, value):
        self.ret_value = value

    def simulate(self, request):
        return self.ret_value


class TestServer(unittest.TestCase):
    def test_query(self):
        with mock.patch('dao.dal.DB.create_request') as db:
            simulator = MockSimulator()
            server = Server(db=db, simulator=simulator)
            request = QueryRequest('bf561866-7264-4c1d-9a7f-e810da7d3ed7', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                                   15, 16, 17, 18)
            response = SimulatorResponse(1, 2, 3, 4, 5, 6, 7, 8)
            db.create_request = Mock(request)
            simulator.set_return_value(response)
            result = server.query(request) == response
            self.assertTrue(result)
