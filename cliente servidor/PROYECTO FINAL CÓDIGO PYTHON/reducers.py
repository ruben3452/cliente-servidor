import zmq, sys
from funciones import *

lista = []

def funcion(data):
    global lista
    lista.append(data)

puerto=5555
ipClient = "localhost"
portClient = "7777"

ctx = zmq.Context()
socketRecv = ctx.socket(zmq.PULL)
port = buscarPuerto(socketRecv,puerto)
print ('mi puerto: ',port)

msj0 = "trabajar"
i=0
while msj0 == "trabajar":
    data = socketRecv.recv_json()
    if data["tarea"]== "trabajar":
        funcion(data["dato"])
    else:
        i+=1
    if i == cantidadMappers-1:
        msj0=""

socketSend = ctx.socket(zmq.PUSH)
socketSend.connect("tcp://{}:{}".format(ipClient,portClient))
socketSend.send_json({"data":lista})
