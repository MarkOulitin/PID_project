class Request:
    def __init__(self, id, timestamp, plc_id, setpoint, p, i, d):
        self.id = id
        self.timestamp = timestamp
        self.plc_id = plc_id
        self.setpoint = setpoint
        self.p = p
        self.i = i
        self.d = d


def row_to_request(row):
    return Request(*tuple(row))
