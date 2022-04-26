import sqlite3
from sqlite3 import Connection
from typing import List
import os

from dao.constants import db_name, plc_create_statement, requests_create_statement, samples_create_statement
from queryrequest import QueryRequest
from recommendation_system.types.recommendation_types import PLC


def initialize(debug=False):
    if debug:
        try:
            os.remove(db_name)
        except:
            pass
    conn = sqlite3.connect(db_name)
    conn.execute(plc_create_statement)
    conn.execute(requests_create_statement)
    conn.execute(samples_create_statement)
    conn.close()


def insert_plcs(PLCs: List[PLC], conn: Connection):  # TODO insert objects
    for plc in PLCs:
        conn.cursor().execute("""
        INSERT OR IGNORE INTO PLC(PlcPath)
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


# def get_samples_since(plc_path: str,
#                       seconds_back: int,
#                       conn: Connection):
#     from_datetime = datetime.datetime.now() - datetime.timedelta(seconds=seconds_back)
#     from_timestamp = int(from_datetime.timestamp())
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT S.SampleId, s.PlcId, ProcessValue, PidValue, SetPoint, Timestamp, P, I, D FROM Samples AS S INNER JOIN PLC ON S.PlcId = PLC.PlcId
#         WHERE PlcPath = ? AND Timestamp >= ?
#         ORDER BY Timestamp
#     """, (plc_path, from_timestamp))
#     result = cursor.fetchall()
#     return list(map(lambda sample: Sample(sample[0], sample[1], sample[2], sample[3], sample[4], sample[5],
#                                           PID(sample[6], sample[7], sample[8])), result))
#
#
# def insert_sample(samples: List[Sample], conn):
#     for sample in samples:
#         conn.cursor().execute("""
#         INSERT OR IGNORE INTO Samples(plcid, processvalue, pidvalue, setpoint, timestamp, p, i, d)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         """, (sample.plc_id, sample.process_value, sample.pid_value, sample.set_point, sample.timestamp, sample.pid.p,
#               sample.pid.i, sample.pid.d))
#     conn.commit()
#     conn.close()


class DB:
    def __init__(self, debug=False):
        initialize(debug)
        # if debug:
        #     acc = []
        #     a = lambda x: np.exp(-np.power(x - 1, 2.) / (2 * np.power(200, 2.)))
        #     for x in range(1000):
        #         acc.append(Sample(1, 1, a(x - 500) * 200, 4.0, 5.0, int(time.time()) - (1000 - x), PID(1., 2., 3.)))
        #     insert_sample(acc, sqlite3.connect(db_name))
        #     insert_plcs([PLC('my.opc')], sqlite3.connect(db_name))

    def create_request(self, request: QueryRequest):
        create_request(request, sqlite3.connect(db_name))

    # def get_samples_since(self, plc_path: str, seconds_back: int = 24 * 60 * 60):
    #     return get_samples_since(plc_path, seconds_back, sqlite3.connect(db_name))
    #
    # def insert_plcs(self, PLCs: List[PLC]):
    #     return insert_plcs(PLCs, sqlite3.connect(db_name))
    #
    # def insert_samples(self, samples: List[Sample]):
    #     return insert_sample(samples)


if __name__ == "__main__":
    db = DB()  # for tomer
    # ree = QueryRequest('8', '8', 0.14, 0.1, '8', 0.1, 0.1, '8', 1.2, 104.5, '8', 0.1, 0.1, 0.1, 0.1, 0.1, 1, 1)
    # db.create_request(ree)
    # plc = PLC('Ayoo')
    # plc2 = PLC('Ayo2')
    # db.insert_plcs([plc, plc2])
    # db.get_samples_since('Ayoo')
    print(db.get_samples_since('Ayoo', 22 * 60))
