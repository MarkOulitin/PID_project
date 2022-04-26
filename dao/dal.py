import os
import sqlite3
from sqlite3 import Connection
from typing import List

from dao.constants import db_name, \
    query_request_create_statement
from queryrequest import QueryRequest


def initialize(debug=False):
    if debug:
        try:
            os.remove(db_name)
        except:
            pass
    conn = sqlite3.connect(db_name)
    conn.execute(query_request_create_statement)
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


def delete_query(query_id: str, conn: Connection):
    conn.cursor().execute("""
    DELETE FROM QueryRequests
    WHERE id = ?
    """, (query_id,))
    conn.commit()
    conn.close()


def get_query_requests_by_plc_path(plc_path: str, conn: Connection) -> List[QueryRequest]:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT PlcPath, P, I, D, SimulationMinutes, SimulationSeconds, SetPoint, id, Timestamp FROM QueryRequests
        WHERE PlcPath = ?
        ORDER BY Timestamp DESC
    """, (plc_path,))
    result = cursor.fetchall()
    return list(
        map(lambda query_request: QueryRequest(query_request[0], query_request[1], query_request[2], query_request[3],
                                               query_request[4], query_request[5], query_request[6], query_request[7],
                                               ),
            result))



class DB:
    def __init__(self, debug=False):
        initialize(debug)

    def create_request(self, request: QueryRequest):
        return insert_query_request(request, sqlite3.connect(db_name))

    def get_query_requests(self, plc_path: str) -> List[QueryRequest]:
        return get_query_requests_by_plc_path(plc_path, sqlite3.connect(db_name))

    def delete_query(self, query_id: str):
        return delete_query(query_id, sqlite3.connect(db_name))


if __name__ == "__main__":
    db = DB()  # for tomer
    # request1 = QueryRequest("1", 2, 3, 4, 5, 6, 'YO')
    # request2 = QueryRequest("2", 2, 3, 4, 5, 6, 'YO')
    # request3 = QueryRequest("3", 2, 3, 4, 5, 6, 'NO')
    # db.create_request(request1)
    # db.create_request(request2)
    # db.create_request(request3)
    # db.delete_query("c5228148-18aa-4884-9025-4f03a7a3b52e")
    for query in db.get_query_requests("1"):
        print(query.id)
