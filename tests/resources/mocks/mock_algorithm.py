import json
import sys

data = json.loads(sys.argv[1])
ret = json.dumps({
    "p": data["set_point"],
    "i": json.loads(data["samples"][0])["pid_value"],
    "d": json.loads(data["samples"][0])["process_value"]
})
print(ret)
