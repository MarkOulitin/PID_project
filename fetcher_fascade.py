from samplers.sampler import Sampler


class FetcherFascade:
    def __init__(self, sampler: Sampler = None):
        self.sampler = sampler

    def fetch_pid(self, pid_path):
        if not self.sampler:
            return 1., 1., 1.,
        value = self.sampler.sample(pid_path)
        return value, value, value

    def fetch_set_point(self, set_point_path):
        if not self.sampler:
            return 1.
        value = self.sampler.sample(set_point_path)
        return value

    def fetch_current_signal(self, value_path):
        if not self.sampler:
            return 1.
        value = self.sampler.sample(value_path)
        return value
