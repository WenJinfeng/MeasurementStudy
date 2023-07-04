# -*- coding: utf-8 -*-
import json
import time

def handler(request):
    tm_st = time.time() * 1000
    # TODO implement

    tmp = {
        'statusCode': 200,
        'body': json.dumps('Hello World!')
    }

    print(tmp)
    return ',timepoint:{}'.format(tm_st)


