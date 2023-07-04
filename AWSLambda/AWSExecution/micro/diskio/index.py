from time import time
import gzip
import os

def handler(event, context):
    tm_st = time() * 1000
    file_size = event['file_size']
    file_write_path = '/tmp/file'

    start = time()
    with open(file_write_path, 'wb') as f:
        f.write(os.urandom(file_size * 1024 * 1024))
    disk_latency = time() - start

    with open(file_write_path, 'rb') as f:
        start = time()
        with gzip.open('/tmp/result.gz', 'wb') as gz:
            gz.writelines(f)
        compress_latency = time() - start

    print("disk_write: {}, compress: {}".format(disk_latency, compress_latency))

    return tm_st

# event1={
#     "file_size":5
# }
# print(lambda_handler(event1, ""))