import logging
import time
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    tm_st = time.time() * 1000
    print('Hello World!')   
    return func.HttpResponse(',timepoint:{}'.format(tm_st))

