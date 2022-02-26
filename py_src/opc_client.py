import OpenOPC
import pywintypes

pywintypes.datetime = pywintypes.TimeType

opc = OpenOPC.client()

servers = opc.servers()
if len(servers) == 0:
    raise Exception("No server found")
server = servers[0]
opc.connect(server)
path_list = sorted(opc.list('*.T*', flat=True))
value = opc.read(path_list[0])  # tuple of value, quality, timestamp

print(path_list)
print(value)


"""
required installs:
OpenOPC (pip install OpenOPC-Python3x)
PyWin32 for Python : (pip install pywin32) or if it doesnt work: http://gestyy.com/etVOqH
"""