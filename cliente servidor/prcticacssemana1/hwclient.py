import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(1):
    print("Sending request %s ..." % request)
    socket.send_json({"operacion":"resta", "op1": 5, "op2": 7})

    #  Get the reply.
    message = socket.recv_json()
    print(message)
