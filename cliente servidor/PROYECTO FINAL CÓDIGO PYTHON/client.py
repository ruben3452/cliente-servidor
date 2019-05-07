import zmq, sys
from funciones import  *

port = "7777"

listaTemporal = []

ctx = zmq.Context()

socketRecv = ctx.socket(zmq.PULL)
socketRecv.bind("tcp://*:{}".format(port))

for numberofReducers in range(cantidadReducers):
    msj = socketRecv.recv_json()
    listaTemporal.append(msj["data"])

print (listaTemporal)
raw_input("finalizar...")
