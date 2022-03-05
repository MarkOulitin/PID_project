from recommendation_types import PID


class Sample:
    def __init__(self, sample_id, plc_id, process_value, pid_value, set_point, timestamp, pid: PID):
        self.sample_id = sample_id
        self.plc_id = plc_id
        self.process_value = process_value
        self.pid_value = pid_value
        self.set_point = set_point
        self.timestamp = timestamp
        self.pid = pid
