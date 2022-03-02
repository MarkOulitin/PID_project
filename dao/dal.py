import sqlite3
from sqlite3 import Connection

from typing import List

from dao.constants import db_name
from dao.plc import row_to_plc
from dao.request import Request, row_to_request
from dao.sample import Sample, row_to_sample


def initialize():
    conn = sqlite3.connect(db_name)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS "PLC" (
            "plcid"	INTEGER,
            "name"	BLOB,
            "plctype"	TEXT,
            "simulation_metadata"	TEXT,
            PRIMARY KEY("plcid")
    );
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS "requests" (
            "requestid"	INTEGER,
            "timestamp"	NUMERIC,
            "plcid"	INTEGER,
            "setpoint"	REAL,
            "P"	REAL,
            "I"	REAL,
            "D"	REAL,
            FOREIGN KEY("plcid") REFERENCES "PLC"("plcid"),
            PRIMARY KEY("requestid")
    );
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS "Samples" (
            "sample_id"	INTEGER,
            "timestamp"	NUMERIC,
            "plcid"	INTEGER,
            "setpoint"	REAL,
            "sensor_value"	REAL,
            PRIMARY KEY("sample_id"),
            FOREIGN KEY("plcid") REFERENCES "PLC"("plcid")
    );
    """)
    return conn


def create_request(request: Request, conn: Connection):
    conn.cursor().execute("""
        INSERT INTO REQUESTS(request_id, timestamp, plcid, setpoint, p, i, d)
        VALUES(?, ?, ?, ?, ?, ?, ?)
    """, (request.plc_id, request.timestamp, request.plc_id, request.setpoint, request.p, request.i, request.d))
    conn.commit()


def get_requests_for_plc(plc_id, conn: Connection):
    conn.cursor().execute("""
        SELECT * FROM REQUESTS WHERE PLCID = ?
    """, (plc_id,))
    rows = conn.cursor().fetchall()
    return list(map(lambda row: row_to_request(row), rows))


def create_samples(samples: List[Sample], conn: Connection):
    for sample in samples:
        conn.cursor().execute("""
            INSERT INTO SAMPLE(sample_id, timestamp, plcid, setpoint, sensor_value)
            VALUES(?, ?, ?, ?, ?)
        """, (sample.sample_id, sample.timestamp, sample.plc_id, sample.setpoint, sample.sensor_value))
    conn.commit()


def get_sample_since(plc_id, timestamp, conn: Connection):
    conn.cursor().execute("""
        SELECT * FROM REQUESTS WHERE PLCID = ? AND TIMESTAMP > timestamp 
    """, (plc_id, timestamp))
    rows = conn.cursor().fetchall()
    return list(map(lambda row: row_to_sample(row), rows))


def create_plc(plc: PLC, conn: Connection):
    conn.cursor().execute("""
        INSERT INTO PLC(plcid, name, plctype,simulation_metadata)
        VALUES(?, ?, ?, ?)
    """, (plc.plc_id, plc.name, plc.type, plc.sim_metadata))
    conn.commit()


def get_all_plcs(conn: Connection):
    conn.cursor().execute("""
        SELECT * FROM PLC 
    """)
    rows = conn.cursor().fetchall()
    return list(map(lambda row: row_to_plc(row), rows))


initialize()
