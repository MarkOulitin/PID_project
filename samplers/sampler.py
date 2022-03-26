import uuid

import OpenOPC
import pywintypes
import time
import datetime

from dao.dal import DB
from recommendation_types import PID
from sample import Sample


class Sampler:
    def __init__(self, db: DB, server=None, paths=None):
        self.stop = False
        self.db = db
        pywintypes.datetime = pywintypes.TimeType

        self.opc = OpenOPC.client()

        servers = opc.servers()
        if len(servers) == 0:
            raise Exception("No server found")
        server = server if server else servers[0]
        self.opc.connect(server)
        self.paths = paths if paths else sorted(self.opc.list('*.T*', flat=True))

    def sample_endless(self, samples_per_second=1):
        while not self.stop:
            for path in self.paths:
                value = self.sample(path)
                sample = Sample(str(uuid.uuid4()),
                                path, # replace with id
                                value,
                                0,
                                0,
                                int(datetime.datetime.now().timestamp()),
                                PID(0, 0, 0))
                self.db.insert_samples([sample])
            time.sleep(samples_per_second)

    def sample(self, path):
        return self.opc.read(path)[0]
