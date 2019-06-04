
from concurrent import futures
import contextlib
import datetime
import logging
import math
import multiprocessing
import time
import socket
import sys
import time
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

#https://github.com/grpc/grpc/blob/master/examples/python/multiprocessing/server.py

_PROCESS_COUNT = multiprocessing.cpu_count()
_THREAD_CONCURRENCY = _PROCESS_COUNT
options = (('grpc.so_reuseport', 1),)


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def __init__(self, i):
        self.i = i

    def SayHello(self, request, context):
        time.sleep(1)
        return helloworld_pb2.HelloReply(message = 'hello {msg} {i}'.format(msg = request.name, i= self.i))

    def SayHelloAgain(self, request, context):
        return helloworld_pb2.HelloReply(message='hello {msg}'.format(msg = request.name))

def serve(i):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_THREAD_CONCURRENCY,), options=options)
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(i), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print "grpc serving is start address is [::]:50051"
    try:
        while True:
            time.sleep(60*60*24) # one day in seconds
    except KeyboardInterrupt:
        server.stop(0)

def main():
    workers = []
    for i in range(_PROCESS_COUNT):
        worker = multiprocessing.Process(target=serve, args=(i,))
        worker.start()
        workers.append(worker)
    for worker in workers:
        worker.join()

if __name__ == '__main__':
    main()