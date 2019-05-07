import zmq, sys
from funciones import *

iterador = 0

def takeData(data,aux):
    limite = 0
    global iterador
    datos = ""
    data.seek(0,2)
    longitud = data.tell()
    partes = longitud//len(mappers)
    print (partes)
    data.seek(iterador,0)
    if iterador+partes < longitud:
        datos= data.read(partes)
        iterador+=partes
    else:
        partes = longitud - iterador
        datos=data.read(partes)
    return datos

ctx = zmq.Context()
aux = 1
data = open("data.data","rb")
for mapper in mappers:
    socketEnvio = ctx.socket(zmq.PUSH)
    socketEnvio.connect("tcp://{}:{}".format(mapper[0],mapper[1]))
    datos = takeData(data,aux)
    socketEnvio.send(datos)
    socketEnvio.close()
    aux+=1
data.close()
