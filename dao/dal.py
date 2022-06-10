import os
import sqlite3
from sqlite3 import Connection
from typing import List

from dao.constants import db_name, \
    query_request_create_statement, samples_create_statement
from queryrequest import QueryRequest
from sampler.sample import Sample


def initialize(debug=False):
    if debug:
        try:
            os.remove(db_name)
        except:
            pass
    conn = sqlite3.connect(db_name)
    conn.execute(query_request_create_statement)
    conn.execute(samples_create_statement)
    conn.close()


def insert_query_request(query_request: QueryRequest, conn: Connection):
    conn.cursor().execute("""
    INSERT INTO QueryRequests(id, PlcPath, P, I, D, SimulationMinutes, SimulationSeconds, SetPoint)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?)
    """, (query_request.id, query_request.plc_path, query_request.p, query_request.i, query_request.d,
          query_request.simulation_minutes, query_request.simulation_seconds, query_request.set_point)
                          )
    conn.commit()
    conn.close()


def get_query_requests_by_plc_path(plc_path: str, conn: Connection) -> List[QueryRequest]:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT PlcPath, P, I, D, SimulationMinutes, SimulationSeconds, SetPoint, id, Timestamp FROM QueryRequests
        WHERE PlcPath = ?
        ORDER BY Timestamp DESC
    """, (plc_path))
    result = cursor.fetchall()
    return list(
        map(lambda query_request: QueryRequest(query_request[0], query_request[1], query_request[2], query_request[3],
                                               query_request[4], query_request[5], query_request[6], query_request[7],
                                               ), result))


def save_sample(sample: Sample, conn: Connection):
    conn.cursor().execute("""
        INSERT INTO Samples(id, Path, Value)
        VALUES(?, ?, ?)
        """, (sample.id, sample.path, sample.value)
                          )
    conn.commit()
    conn.close()


class DB:
    def __init__(self, debug=False):
        initialize(debug)

    def create_request(self, request: QueryRequest):
        return insert_query_request(request, sqlite3.connect(db_name))

    def get_query_requests(self, plc_path: str) -> List[QueryRequest]:
        return get_query_requests_by_plc_path(plc_path, sqlite3.connect(db_name))

    # Uncomment when the factory is ready to transition to OPC-UA
    # def save_sample(self, sample: Sample):
    #     return save_sample(sample, sqlite3.connect(db_name))


if __name__ == "__main__":
    db = DB()  # for tomer
    sample1 = Sample("path", "value")
    sample2 = Sample("path2", "value2")
    db.save_sample(sample1)
    db.save_sample(sample2)
    # request1 = QueryRequest("1", 2, 3, 4, 5, 6, 'YO')
    # request2 = QueryRequest("2", 2, 3, 4, 5, 6, 'YO')
    # request3 = QueryRequest("3", 2, 3, 4, 5, 6, 'NO')
    # db.create_request(request1)
    # db.create_request(request2)
    # db.create_request(request3)
    # for query in db.get_query_requests("1"):
    #     print(query.id)
