import logging
import time
import azure.functions as func
import gzip
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    # logging.info('Python HTTP trigger function processed a request.')
    tm_st = time.time() * 1000
    name = req.params.get('name')
    
    file_size = int(name)
    
    
    file_write_path = '/tmp/file'

    start = time.time()
    with open(file_write_path, 'wb') as f:
        f.write(os.urandom(file_size * 1024 * 1024))
    disk_latency = time.time() - start

    with open(file_write_path, 'rb') as f:
        start = time.time()
        with gzip.open('/tmp/result.gz', 'wb') as gz:
            gz.writelines(f)
        compress_latency = time.time() - start

    print("disk_write: {}, compress: {}".format(disk_latency, compress_latency))
  
    return func.HttpResponse(',timepoint:{}'.format(tm_st))

