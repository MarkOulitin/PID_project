import unittest

from dao.dal import DB
from queryrequest import QueryRequest
from sampler.sample import Sample


def generate_sample():
    return Sample('path', 'value', 'testID')


def list_contains_by_id(lst, obj):
    for item in lst:
        if item.id == obj.id:
            return True
    return False


class TestDB(unittest.TestCase):
    def test_insert_query(self):
        db = DB()
        query = QueryRequest('path', 'p', 'i', 'd', 1, 1, 1)
        db.insert_query_request(query)
        fetched_queries = db.get_query_requests_by_path('path')
        self.assertTrue(list_contains_by_id(fetched_queries, query))
        db.delete_query_request(query.id)

    def test_delete_query(self):
        db = DB()
        query = QueryRequest('path', 'p', 'i', 'd', 1, 1, 1)
        db.insert_query_request(query)
        fetched_queries = db.get_query_requests_by_path('path')
        self.assertTrue(list_contains_by_id(fetched_queries, query))
        db.delete_query_request(query.id)
        fetched_queries = db.get_query_requests_by_path('path')
        self.assertFalse(list_contains_by_id(fetched_queries, query))

    def test_fetch_queries(self):
        db = DB()
        query = QueryRequest('path', 'p', 'i', 'd', 1, 1, 1)
        db.insert_query_request(query)
        fetched_queries = db.get_query_requests_by_path('path')
        self.assertTrue(list_contains_by_id(fetched_queries, query))
        db.delete_query_request(query.id)