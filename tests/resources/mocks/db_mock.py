from typing import List

from dao.dal import DB
from queryrequest import QueryRequest
from sample import Sample


class DbMock(DB):
    def __init__(self):
        super().__init__()
        self.plc_path = None
        self.seconds_back = None
        self.samples: List[Sample] = []

    def create_request(self, request: QueryRequest):
        pass

    def get_samples_since(self, plc_path: str, seconds_back: int = 24 * 60 * 60):
        assert self.seconds_back == seconds_back
        assert self.plc_path == plc_path
        return self.samples

    def set_expected_values(self, plc_path, seconds_back, samples: List[Sample]):
        self.plc_path = plc_path
        self.seconds_back = seconds_back
        self.samples = samples
