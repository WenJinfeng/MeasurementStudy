import json
from urllib.request import urlopen
from time import time


def handler(event, context):
    tm_st = time() * 1000

    link = event['link']  

    start = time()
    f = urlopen(link)
    data = f.read().decode("utf-8")
    network = time() - start

    start = time()
    json_data = json.loads(data)
    str_json = json.dumps(json_data, indent=4)
    latency = time() - start

    print(str_json)

    return tm_st
