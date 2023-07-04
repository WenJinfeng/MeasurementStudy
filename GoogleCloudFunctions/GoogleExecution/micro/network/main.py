import json
from urllib.request import urlopen
from time import time


def handler(request):
    tm_st = time() * 1000
    request = request.get_json()
    link = request['link']  

    start = time()
    f = urlopen(link)
    data = f.read().decode("utf-8")
    network = time() - start

    start = time()
    json_data = json.loads(data)
    str_json = json.dumps(json_data, indent=4)
    latency = time() - start

    print(str_json)

    return ',timepoint:{}'.format(tm_st)
