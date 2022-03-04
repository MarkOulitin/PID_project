import uuid

from flask import Request
import json


class QueryRequest:
    def __init__(self,
                 id,
                 value_path,
                 value_min,
                 value_max,
                 set_point_path,
                 set_point_min,
                 set_point_max,
                 pid_path,
                 pid_min,
                 pid_max,
                 pid_value_path,
                 pid_value_min,
                 pid_value_max,
                 p,
                 i,
                 d,
                 simulation_minutes,
                 simulation_seconds):
        self.id = id
        self.value_path = value_path
        self.value_min = value_min
        self.value_max = value_max
        self.set_point_path = set_point_path
        self.set_point_min = set_point_min
        self.set_point_max = set_point_max
        self.pid_path = pid_path
        self.pid_min = pid_min
        self.pid_max = pid_max
        self.pid_value_path = pid_value_path
        self.pid_value_min = pid_value_min
        self.pid_value_max = pid_value_max
        self.p = p
        self.i = i
        self.d = d
        self.simulation_minutes = simulation_minutes
        self.simulation_seconds = simulation_seconds


def row_to_request(row):
    return QueryRequest(*tuple(row))


def flask_request_to_request(request: Request):
    args = request.args
    query_data, pid_values, time_value = json.loads(args['queryData']), \
                                      json.loads(args['pidValues']), \
                                      json.loads(args['timeValue'])
    return QueryRequest(
        id=str(uuid.uuid4()),
        value_path=query_data['valPath']['path'],
        value_min=query_data['valPath']['minVal'],
        value_max=query_data['valPath']['maxVal'],
        set_point_path=query_data['setpointPath']['path'],
        set_point_min=query_data['setpointPath']['minVal'],
        set_point_max=args.get("set_point_max"),
        pid_path=args.get("pid_path"),
        pid_min=args.get("pid_min"),
        pid_max=args.get("pid_max"),
        pid_value_path=args.get("pid_value_path"),
        pid_value_min=args.get("pid_value_min"),
        pid_value_max=args.get("pid_value_max"),
        p=args.get("p"),
        i=args.get("i"),
        d=args.get("d"),
        simulation_minutes=args.get("simulation_minutes"),
        simulation_seconds=args.get("simulation_seconds")
    )
