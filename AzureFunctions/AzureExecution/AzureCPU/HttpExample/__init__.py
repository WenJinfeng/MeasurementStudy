import logging
import time
import azure.functions as func
from numpy import matrix, linalg, random


def linpack(n):
    # LINPACK benchmarks
    ops = (2.0 * n) * n * n / 3.0 + (2.0 * n) * n

    # Create AxA array of random numbers -0.5 to 0.5
    A = random.random_sample((n, n)) - 0.5
    B = A.sum(axis=1)

    # Convert to matrices
    A = matrix(A)
    B = matrix(B.reshape((n, 1)))

    # Ax = B
    start = time.time()
    x = linalg.solve(A, B)
    latency = time.time() - start

    mflops = (ops * 1e-6 / latency)

    result = {
        'mflops': mflops,
        'latency': latency
    }

    return result


def main(req: func.HttpRequest) -> func.HttpResponse:
    # logging.info('Python HTTP trigger function processed a request.')
    tm_st = time.time() * 1000

    name = req.params.get('name')

    if name:
        result = linpack(int(name))
        return func.HttpResponse(',timepoint:{}'.format(tm_st))
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )



