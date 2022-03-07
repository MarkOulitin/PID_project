from fetcher_fascade import FetcherFascade


class FetcherMock(FetcherFascade):
    def __init__(self):
        super().__init__()
        self.value = None
        self.value_path = None
        self.set_point = None
        self.set_point_path = None
        self.pid = None
        self.pid_path = None

    def fetch_pid(self, pid_path):
        assert self.pid_path == pid_path
        return self.pid.p, self.pid.i, self.pid.d

    def fetch_set_point(self, set_point_path):
        assert self.set_point_path == set_point_path
        return self.set_point

    def fetch_current_signal(self, value_path):
        assert self.value_path == value_path
        return self.value

    def set_ret_values(self, pid_path, pid, set_point_path, set_point, value_path, value):
        self.pid_path = pid_path
        self.pid = pid
        self.set_point_path = set_point_path
        self.set_point = set_point
        self.value_path = value_path
        self.value = value