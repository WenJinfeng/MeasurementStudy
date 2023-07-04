from numpy import matrix, linalg, random
from time import time
import json

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
    start = time()
    x = linalg.solve(A, B)
    latency = time() - start

    mflops = (ops * 1e-6 / latency)

    result = {
        'mflops': mflops,
        'latency': latency
    }

    return result


def handler(event, context):
    tm_st = time() * 1000
    event = json.loads(event)
    n = int(event['n'])
    result = linpack(n)
    print(result)
    return tm_st

# event1={
#     "n": 20
# }
# lambda_handler(event1, "")