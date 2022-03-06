import datetime
import sqlite3
from numbers import Number
from sqlite3 import Connection
from typing import List

import numpy as np

from dao.constants import db_name, plc_create_statement, requests_create_statement, samples_create_statement
from queryrequest import QueryRequest
from recommendation_types import PLC, PID
from sample import Sample


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
    from_datetime = datetime.datetime.now() - datetime.timedelta(seconds=seconds_back)  # TODO check type Number
    from_timestamp = from_datetime.strftime('%Y-%m-%d %H:%M:%S')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM  PLC
        WHERE PlcPath = ? AND Timestamp >= ?
        ORDER BY Timestamp
    """, (plc_path, from_timestamp))
    result = cursor.fetchall()
    return result  # TODO maybe reverse?


class DB:
    def __init__(self):
        initialize()

    def create_request(self, request: QueryRequest):
        create_request(request, sqlite3.connect(db_name))

    def get_samples_since(self, plc_path: str, seconds_back: Number = 24 * 60 * 60):
        acc = []
        for x in range(1000):
            acc.append(Sample(1, 2, np.sin(float(x) / 50) * 30, 4.0, 5.0, 90182573 + x, PID(1., 2., 3.)))
        return acc
        # get_samples_since(plc_path, seconds_back, sqlite3.connect(db_name))
