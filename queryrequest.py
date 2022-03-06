import json
import uuid

from flask import Request


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
        value_path=query_data['valPath'].get('path'),
        value_min=float(query_data['valPath'].get('minVal')),
        value_max=float(query_data['valPath'].get('maxVal')),
        set_point_path=query_data['setpointPath'].get('path'),
        set_point_min=float(query_data['setpointPath'].get('minVal')),
        set_point_max=float(query_data['setpointPath'].get('maxVal')),
        pid_path=query_data["pidPath"].get("path"),
        pid_min=float(query_data["pidPath"].get("minVal")),
        pid_max=float(query_data["pidPath"].get("maxVal")),
        pid_value_path=query_data["pidValuePath"].get("path"),
        pid_value_min=float(query_data["pidValuePath"].get("minVal")),
        pid_value_max=float(query_data["pidValuePath"].get("maxVal")),
        p=float(pid_values.get("pVal")),
        i=float(pid_values.get("iVal")),
        d=float(pid_values.get("dVal")),
        simulation_minutes=int(time_value.get("minutes")),
        simulation_seconds=int(time_value.get("seconds"))
    )
