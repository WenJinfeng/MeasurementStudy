
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


def handler(event, context):
    """
    Main handler.
    :param event: event data.
    :param context: unused context.
    """
    tm_st = time.time() * 1000
    for _ in range(TESTS):
        fibonacci(event['index'])
    duration = time.time() - tm_st
    print(duration)
    return tm_st


