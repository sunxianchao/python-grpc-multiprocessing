import grpc
import time
import helloworld_pb2
import helloworld_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='czl'))
    print("Greeter client received: " + response.message)
    #response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='daydaygo'))
    #print("Greeter client received: " + response.message)

if __name__ == '__main__':
    print "start"+ str(time.time())
    for i in range(100):
        run()
    print "end"+ str(time.time())