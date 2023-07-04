
import azure.functions as func
import time
import json


TESTS = 1


def fibonacci(index):
    """
    Recursive function that calculates Fibonacci sequence.
    :param index: the n-th element of Fibonacci sequence to calculate.
    :return: n-th element of Fibonacci sequence.
    """

    if index <= 1:
        return index
    return fibonacci(index - 1) + fibonacci(index - 2)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Main handler.
    :param event: event data.
    :param context: unused context.
    """
    tm_st = time.time() * 1000
    name = req.params.get('name')
    index = int(name)

    for _ in range(TESTS):
        fibonacci(index)
    duration = time.time() - tm_st
    print(duration)
    
    return func.HttpResponse(',timepoint:{}'.format(tm_st))

