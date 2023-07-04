# -*- coding: utf-8 -*-
import json
import time

def handler(event, context):
    tm_st = time.time() * 1000
    # TODO implement
    tmp = {
        'statusCode': 200,
        'body': json.dumps('Hello World!')
    }
    print(tmp)
    return tm_st


