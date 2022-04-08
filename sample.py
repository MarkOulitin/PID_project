from recommendation_types import PID, SimulationData


class Sample:
    def __init__(self, sample_id, plc_id, process_value, pid_value, set_point, timestamp, pid: PID):
        self.sample_id = sample_id
        self.plc_id = plc_id
        self.process_value = process_value
        self.pid_value = pid_value
        self.set_point = set_point
        self.timestamp = timestamp
        self.pid = pid

    def to_simulation_data(self) -> SimulationData:
        return SimulationData(timestamp=self.timestamp, process_value=self.process_value, set_point=self.set_point,
                              out_value=self.pid_value, pid=self.pid)
