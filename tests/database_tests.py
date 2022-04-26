import unittest

from dao.dal import DB
from queryrequest import QueryRequest


def generate_fresh_request(plc_path: str):
    return QueryRequest(plc_path, 2, 3, 4, 5, 6, "7")


class TestDatabase(unittest.TestCase):
    def test_insert_1(self):
        db = DB()
        request = generate_fresh_request("1")
        db.create_request(request)
        fetched = db.get_query_requests(request.plc_path)
        # found = False
        for req in fetched:
            if req.id == request.id:
                found = True
        assert found
        db.delete_query(request.id)

    def test_insert_2(self):
        db = DB()
        request = generate_fresh_request("1")
        fetched = db.get_query_requests(request.plc_path)
        found = False
        for req in fetched:
            if req.id == request.id:
                found = True
        assert not found

    def test_insert_3(self):
        db = DB()
        request = generate_fresh_request("1")
        request2 = generate_fresh_request("2")
        db.create_request(request)
        fetched = db.get_query_requests(request.plc_path)
        found = False
        for req in fetched:
            if req.id == request2.id:
                found = True
        assert not found
        db.delete_query(request.id)

    def test_get_1(self):
        db = DB()
        request = generate_fresh_request("1")
        fetched = db.get_query_requests(request.plc_path)
        assert len(fetched) == 0

    def test_get_2(self):
        db = DB()
        request = generate_fresh_request("1")
        db.create_request(request)
        fetched = db.get_query_requests(request.plc_path)
        found = False
        for req in fetched:
            if req.id == request.id:
                found = True
        assert found
        db.delete_query(request.id)

    def test_delete(self):
        db = DB()
        request = generate_fresh_request("1")
        db.create_request(request)
        fetched = db.get_query_requests(request.plc_path)
        found = False
        for req in fetched:
            if req.id == request.id:
                found = True
        assert found
        db.delete_query(request.id)
        fetched = db.get_query_requests(request.plc_path)
        found = False
        for req in fetched:
            if req.id == request.id:
                found = True
        assert not found
