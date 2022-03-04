import sqlite3
from numbers import Number
from sqlite3 import Connection

from typing import List

from dao.constants import db_name, plc_create_statement, requests_create_statement, samples_create_statement
from queryrequest import QueryRequest, row_to_request


def initialize():
    conn = sqlite3.connect(db_name)
    conn.execute(plc_create_statement)
    conn.execute(requests_create_statement)
    conn.execute(samples_create_statement)
    conn.close()


def insert_plcs(PLCs: List[PLC]):  # TODO insert objects
    pass


def create_request(request: QueryRequest, conn: Connection):  # TODO insert request object
    pass
    # conn.cursor().execute("""
    #     INSERT INTO REQUESTS(request_id, timestamp, plcid, setpoint, p, i, d)
    #     VALUES(?, ?, ?, ?, ?, ?, ?,)
    # """, (request.plc_id, request.timestamp, request.plc_id, request.setpoint, request.p, request.i, request.d))
    # conn.commit()
    # conn.close()


def get_samples_since(plc_path: str,
                      seconds_back: Number,
                      conn: Connection):  # TODO get samples 'seconds_back' seconds from the past until now, ordered by timestamp. return object of type SimulationData
    return []


class DB:
    def __init__(self):
        initialize()

    def create_request(self, request: QueryRequest):
        create_request(request, sqlite3.connect(db_name))

    def get_samples_since(self, plc_path: str, seconds_back: Number = 24 * 60 * 60):
        get_samples_since(plc_path, seconds_back, sqlite3.connect(db_name))
