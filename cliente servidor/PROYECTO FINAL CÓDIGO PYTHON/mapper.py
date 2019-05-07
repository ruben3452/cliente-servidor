#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zmq, sys, time, json
from funciones import *

def condicion1():
    return 1

def condicion2():
    return 0

def condicion3():
    return 0

puerto=4444

ctx = zmq.Context()
socketRecv = ctx.socket(zmq.PULL)
port = buscarPuerto(socketRecv,puerto)
print ('mi puerto',port)
data = socketRecv.recv()
socketSend0 = ctx.socket(zmq.PUSH)
socketSend1 = ctx.socket(zmq.PUSH)
socketSend2 = ctx.socket(zmq.PUSH)
socketSend0.connect("tcp://{}:{}".format(reducers[0][0],reducers[0][1]))
socketSend1.connect("tcp://{}:{}".format(reducers[1][0],reducers[1][1]))
socketSend2.connect("tcp://{}:{}".format(reducers[2][0],reducers[2][1]))

for dato in data:
    if condicion1():        
        socketSend0.send_json({"tarea":"trabajar","dato":data})
    elif condicion2():        
        socketSend1.send_json({"tarea":"trabajar","dato":data})
    else:        
        socketSend2.send_json({"tarea":"trabajar","dato":data})

socketSend0.send_json({"tarea":"detener","dato":0})
socketSend1.send_json({"tarea":"detener","dato":0})
socketSend2.send_json({"tarea":"detener","dato":0})
