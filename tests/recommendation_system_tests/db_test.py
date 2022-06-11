import unittest

from dao.dal import DB


class TestModelFitting(unittest.TestCase):

    def db_sample_test(self):
        db = DB()
        sample1 = Sample("path", "value")
        sample2 = Sample("path2", "value2")
        db.save_sample(sample1)
        db.save_sample(sample2)
        self.assertEqual(True, True)

    def db_query_request_test(self):
        db = DB()
        request1 = QueryRequest("1", 2, 3, 4, 5, 6, 'YO')
        request2 = QueryRequest("2", 2, 3, 4, 5, 6, 'YO')
        request3 = QueryRequest("3", 2, 3, 4, 5, 6, 'NO')
        db.create_request(request1)
        db.create_request(request2)
        db.create_request(request3)
        for query in db.get_query_requests("1"):
            print(query.id)
        self.assertEqual(True, True)
