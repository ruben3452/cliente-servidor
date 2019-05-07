
import time
import zmq

context = zmq.Context()
s = context.socket(zmq.REP)
s.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = s.recv_json()
    print(message)

    resultado = 0
    if message["operacion"] == "suma":
        resultado = message["op1"] + message["op2"]
    elif message["operacion"] == "resta":
        resultado = message["op1"] - message["op2"]
    #  Do some 'work'

    #  Send reply back to client
    s.send_json({"resultado":resultado, "error": False})
