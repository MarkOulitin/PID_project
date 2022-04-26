import json
import string
import uuid
from random import choice

from flask import Request


def random_path():
    letters = string.ascii_lowercase
    return (''.join(choice(letters) for i in range(3))) + "/" + (''.join(choice(letters) for i in range(3))) + "/" + (
        ''.join(choice(letters) for i in range(3)))


class QueryRequest:
    def __init__(self,
                 plc_path: str,
                 p: float,
                 i: float,
                 d: float,
                 simulation_minutes: int,
                 simulation_seconds: int,
                 set_point: str,
                 id=None):
        self.id = id
        self.plc_path = plc_path
        self.p = p
        self.i = i
        self.d = d
        self.simulation_minutes = simulation_minutes
        self.simulation_seconds = simulation_seconds
        self.set_point = set_point
        self.id = id if id else str(uuid.uuid4())


def row_to_request(row):
    return QueryRequest(*tuple(row))


def flask_request_to_request(request: Request):
    args = request.form
    plc_path, pid_values, time_value, set_point = json.loads(args['plcPath']), \
                                                  json.loads(args['pidValues']), \
                                                  json.loads(args['timeValue']), \
                                                  json.loads(args['setPoint'])
    set_point = ""
    try:
        set_point = float(set_point)

    except:
        set_point = ""

    return QueryRequest(
        id=str(uuid.uuid4()),
        plc_path=plc_path,
        p=float(pid_values.get("pVal")),
        i=float(pid_values.get("iVal")),
        d=float(pid_values.get("dVal")),
        simulation_minutes=int(time_value.get("minutes")),
        simulation_seconds=int(time_value.get("seconds")),
        set_point=set_point
    )
