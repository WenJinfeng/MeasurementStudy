
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


def handler(request):
    """
    Main handler.
    :param event: event data.
    :param context: unused context.
    """
    tm_st = time.time() * 1000
    request = request.get_json()
    for _ in range(TESTS):
        fibonacci(request['index'])
    duration = time.time() - tm_st
    print(duration)
    return ',timepoint:{}'.format(tm_st)


