import datetime
import sqlite3
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


def insert_plcs(PLCs: List[PLC], conn: Connection):  # TODO insert objects
    for plc in PLCs:
        conn.cursor().execute("""
        INSERT INTO PLC(PlcPath)
        VALUES(?)
        """, (plc.name,))
    conn.commit()
    conn.close()


def create_request(request: QueryRequest, conn: Connection):  # TODO insert request object
    conn.cursor().execute("""
        INSERT INTO REQUESTS(id, ValuePath, ValueMin, ValueMax,SetPointPath, SetPointMin, SetPointMax,PidPath, PidMin, PidMax,PidValuePath,PidValueMin,PidValueMax, p, i, d,SimulationMinutes,SimulationSeconds)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        request.id, request.value_path, request.value_min, request.value_max, request.set_point_path,
        request.set_point_min,
        request.set_point_max, request.pid_path, request.pid_min, request.pid_max, request.pid_value_path,
        request.pid_value_min, request.pid_value_max, request.p, request.i, request.d, request.simulation_minutes,
        request.simulation_seconds))
    conn.commit()
    conn.close()


def get_samples_since(plc_path: str,
                      seconds_back: int,
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

    def get_samples_since(self, plc_path: str, seconds_back: int = 24 * 60 * 60):
        acc = []
        a = lambda x: np.exp(-np.power(x - (1), 2.) / (2 * np.power(200, 2.)))
        for x in range(1000):
            acc.append(Sample(1, 2, a(x - 500) * 200, 4.0, 5.0, 90182573 + x, PID(1., 2., 3.)))
        return acc
        # print(get_samples_since(plc_path, seconds_back, sqlite3.connect(db_name)))

    def insert_plcs(self, PLCs: List[PLC]):
        insert_plcs(PLCs, sqlite3.connect(db_name))


if __name__ == "__main__":
    db = DB()  # for tomer
    # ree = QueryRequest('8', '8', 0.14, 0.1, '8', 0.1, 0.1, '8', 1.2, 104.5, '8', 0.1, 0.1, 0.1, 0.1, 0.1, 1, 1)
    # db.create_request(ree)
    # plc = PLC('Ayoo')
    # plc2 = PLC('Ayo2')
    # db.insert_plcs([plc, plc2])
    db.get_samples_since('Ayoo')

