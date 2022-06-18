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
    db = DB()

    def test_insert_query(self):
        query = QueryRequest('path', 'p', 'i', 'd', 1, 1, 1)
        self.db.insert_query_request(query)
        fetched_queries = self.db.get_query_requests_by_path('path')
        self.assertTrue(list_contains_by_id(fetched_queries, query))
        self.db.delete_query_request(query.id)

    def test_insert_not_unique_query(self):
        query1 = QueryRequest('path', 'p', 'i', 'd', 1, 1, 1)
        query2 = QueryRequest('path', 'p', 'i', 'd', 1, 1, 1)
        self.db.insert_query_request(query1)
        self.db.insert_query_request(query2)
        self.assertRaises(Exception, self.db.delete_query_request(query2.id))
        self.db.delete_query_request(query1.id)
        self.db.delete_query_request(query2.id)

    def test_delete_query(self):
        query = QueryRequest('path', 'p', 'i', 'd', 1, 1, 1)
        self.db.insert_query_request(query)
        fetched_queries = self.db.get_query_requests_by_path('path')
        self.assertTrue(list_contains_by_id(fetched_queries, query))
        self.db.delete_query_request(query.id)
        fetched_queries = self.db.get_query_requests_by_path('path')
        self.assertFalse(list_contains_by_id(fetched_queries, query))
        self.db.delete_query_request(query.id)

    def test_fetch_queries(self):
        query = QueryRequest('path', 'p', 'i', 'd', 1, 1, 1)
        self.db.insert_query_request(query)
        fetched_queries = self.db.get_query_requests_by_path('path')
        self.assertTrue(list_contains_by_id(fetched_queries, query))
        self.db.delete_query_request(query.id)

    def test_insert_sample(self):
        sample = Sample('path', 'value')
        self.db.insert_sample(sample)
        fetched_sample = self.db.get_sample(sample.id)
        self.assertTrue(fetched_sample.id == sample.id)
        self.db.delete_sample(sample.id)

    def test_insert_not_unique_sample(self):
        sample1 = Sample('path', 'value', '51010')
        sample2 = Sample('path', 'value', '51010')
        self.db.insert_sample(sample1)
        with self.assertRaises(Exception) as context:
            self.db.insert_sample(sample2)
        self.assertTrue('UNIQUE' in str(context.exception))
        self.db.delete_sample(sample1.id)

    def test_delete_sample(self):
        sample = Sample('path', 'value')
        with self.assertRaises(Exception) as context:
            self.db.get_sample(sample.id)
        self.assertTrue('NoneType' in str(context.exception))

    def test_fetch_samples(self):
        sample = Sample('path', 'value')
        self.db.insert_sample(sample)
        fetched_sample = self.db.get_sample(sample.id)
        self.assertTrue(fetched_sample.id == sample.id)
