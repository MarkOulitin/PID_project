import OpenOPC
import pywintypes

from dao.dal import DB


class Sampler:
    def __init__(self, db: DB):
        pywintypes.datetime = pywintypes.TimeType
        self.opc = OpenOPC.client()
        self.db = db

        servers = opc.servers()
        if len(servers) == 0:
            raise Exception("No server found")
        server = servers[0]
        self.opc.connect(server)
        self.path_list = sorted(opc.list('*.T*', flat=True))

    def sample(self):
        values = [(path, self.opc.read(path)) for path in self.path_list]
        for path, value in values:
            self.db.save_sample(path, value)


"""
required installs:
OpenOPC (pip install OpenOPC-Python3x)
PyWin32 for Python : (pip install pywin32) or if it doesnt work: http://gestyy.com/etVOqH
"""