import json
import string
import uuid
from random import choice, randint
from numbers import Number

from flask import Request


def random_path():
    letters = string.ascii_lowercase
    return (''.join(choice(letters) for i in range(3))) + "/" + (''.join(choice(letters) for i in range(3))) + "/" + (
        ''.join(choice(letters) for i in range(3)))


class QueryRequest:
    def __init__(self,
                 plc_path,
                 p,
                 i,
                 d,
                 simulation_minutes,
                 simulation_seconds,
                 id=str(uuid.uuid4())):
        self.id = id
        self.plc_path = plc_path
        self.p = p
        self.i = i
        self.d = d
        self.simulation_minutes = simulation_minutes
        self.simulation_seconds = simulation_seconds


def row_to_request(row):
    return QueryRequest(*tuple(row))


def flask_request_to_request(request: Request):
    args = request.form
    plc_path, pid_values, time_value = json.loads(args['plcPath']), \
                                         json.loads(args['pidValues']), \
                                         json.loads(args['timeValue'])
    return QueryRequest(
        id=str(uuid.uuid4()),
        plc_path=plc_path,
        p=float(pid_values.get("pVal")),
        i=float(pid_values.get("iVal")),
        d=float(pid_values.get("dVal")),
        simulation_minutes=int(time_value.get("minutes")),
        simulation_seconds=int(time_value.get("seconds"))
    )
