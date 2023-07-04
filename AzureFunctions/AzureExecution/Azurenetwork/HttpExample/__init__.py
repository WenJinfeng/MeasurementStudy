import logging
import time
import azure.functions as func
from urllib.request import urlopen
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    # logging.info('Python HTTP trigger function processed a request.')
    tm_st = time.time() * 1000
    name = req.params.get('name')
    
    link = name
    
    start = time.time()
    f = urlopen(link)
    data = f.read().decode("utf-8")
    network = time.time() - start

    start = time.time()
    json_data = json.loads(data)
    str_json = json.dumps(json_data, indent=4)
    latency = time.time() - start

    print(str_json)
  
    return func.HttpResponse(',timepoint:{}'.format(tm_st))

