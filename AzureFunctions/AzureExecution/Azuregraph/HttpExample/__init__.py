
import azure.functions as func
import datetime
import igraph
from time import time

def main(req: func.HttpRequest) -> func.HttpResponse:
    tm_st = time() * 1000
    
    size = 1000

    graph_generating_begin = datetime.datetime.now()
    graph = igraph.Graph.Barabasi(size, 10)
    graph_generating_end = datetime.datetime.now()

    process_begin = datetime.datetime.now()
    result = graph.pagerank()
    process_end = datetime.datetime.now()

    graph_generating_time = (graph_generating_end - graph_generating_begin) / datetime.timedelta(microseconds=1)
    process_time = (process_end - process_begin) / datetime.timedelta(microseconds=1)

    temp =  {
            'result': result[0],
            'measurement': {
                'graph_generating_time': graph_generating_time,
                'compute_time': process_time
            }
    }
    print(temp)

  
    return func.HttpResponse(',timepoint:{}'.format(tm_st))

