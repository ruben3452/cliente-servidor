#!/usr/bin/python

import zmq
import random
import sys
import time
import hashlib
import json
import os
import base64
import time


def LimIngSer(ml, ls, key):
    if ml < ls:
        return key > ml and key <= ls
    else:
        return key > ml or key <= ls

def LimToq(ml, lp, key):
    if ml < lp:
        return key > ml and key <= lp
    else:
        return key > ml or key <= lp

def OperacionesToquens(message, lb, ub):

    if message["op"] == "adicionar":

        if LimToq(lb, ub, message["toquen"]):
            print ("\nSe va A Recibir toquen: " + message["toquen"])
            archi={message["toquen"]:message["datos"]}
            json_data = json.dumps(archi, indent=1)
            with open("toquen/"+message["toquen"]+".json", 'w') as output:
                output.write(json_data)
        else:
            print ("\nTransferir: " + message["toquen"])
            s2 = context.socket(zmq.PAIR)
            s2.connect("tcp://"+hostsucc+":" + portsucc)
            s2.send_json(message)
            s2.close()

    elif message["op"] == "completa":

        if LimToq(lb, ub, message["indice"]):
            print ("\nSe va A Descargar toquen: " + message["indice"])
            with open("toquen/"+message["indice"]+".json", 'r') as input:
                new_json_data = json.load(input)
                fstring = new_json_data[message["indice"]]
            s1 = context.socket(zmq.PAIR)#ace la coneccion con el servidor
            s1.connect("tcp://localhost:"+message["myport"]) 
            s1.send_json({ "completa": fstring })
            s1.close()

        else:
            print ("\nTransferir: " + message["indice"])
            s2 = context.socket(zmq.PAIR)
            s2.connect("tcp://"+hostsucc+":" + portsucc)
            s2.send_json(message)
            s2.close()
        

configFile = open(sys.argv[1],'r')
config = json.load(configFile)


context = zmq.Context()

# configuracion Local
myhost = config['host']
porhost = config['porhost']
mySocket = context.socket(zmq.PAIR)
#mySocket.bind("tcp://*:"+ porhost )
mySocket.bind("tcp://"+myhost+":"+ porhost )

# configuracion Server Conocido
hostser = config['hostser']
porhostser = config['porhostser']

# configuracion Comunicacion clientes
hostclie = config['hostclie']
portclie = config['portclie']
clientSocket = context.socket(zmq.PAIR)
#clientSocket.bind("tcp://*:"+ portclie )
clientSocket.bind("tcp://"+hostclie+":"+ portclie )


nodeName = hashlib.sha256(myhost.encode('utf-8')).hexdigest()
print("Server Toquen: {}".format(nodeName))
print("HostIp: {}".format(myhost))

MyLim = nodeName
LimPred=""
limsucc=""
hostsucc=""
portsucc=""
hostpre=""
portpre=""

if myhost==hostser:
    LimPred = nodeName
    limsucc = nodeName
    hostsucc=myhost
    portsucc=porhost
    print("\nRango ({},{}]".format(LimPred,MyLim))
else:
    succSocket1 = context.socket(zmq.PAIR)
    succSocket1.connect("tcp://"+hostser+":" + porhostser)
    succSocket1.send_json({'op': 'new', 'key': nodeName, 'key1': myhost, 'key2': porhost,'key3': hostser, 'key4': porhostser})
    succSocket1.close()


poller = zmq.Poller()
poller.register(mySocket, zmq.POLLIN)
poller.register(clientSocket, zmq.POLLIN)

while True:
    socks = dict(poller.poll())
    if mySocket in socks and socks[mySocket] == zmq.POLLIN:
        m = mySocket.recv_json()

        if m['op'] == 'new':
            key = m['key']
            if LimIngSer(MyLim, limsucc, key):

                if hostpre == "":

                    hostsucc=m['key1']
                    portsucc=m['key2']
                    hostpre=m['key1']
                    portpre=m['key2']
                                      
                    succSocket2 = context.socket(zmq.PAIR)
                    succSocket2.connect("tcp://"+hostsucc+":" + portsucc)
                    succSocket2.send_json({'op': 'uppred','key1': myhost, 'key2': porhost})
                    succSocket2.send_json({'op':'upsucc','key': nodeName,'key1': myhost,'key2': porhost})
                    succSocket2.close()

                    LimPred = key

                else:

                    succSocket2 = context.socket(zmq.PAIR)
                    succSocket2.connect("tcp://"+hostsucc+":" + portsucc)
                    succSocket2.send_json({'op': 'uppred','key1': m['key1'], 'key2': m['key2']})
                    succSocket2.close()

                    succSocket2 = context.socket(zmq.PAIR)
                    #print(m['key1'])
                    succSocket2.connect("tcp://"+m['key1']+":" + m['key2'])
                    succSocket2.send_json({'op': 'uppred','key1': myhost, 'key2': porhost})
                    succSocket2.send_json({'op':'upsucc','key': nodeName,'key1': hostsucc,'key2': portsucc})
                    succSocket2.close()

                    hostsucc=m['key1']
                    portsucc=m['key2']
                    


                print("\nNuevo Rango ({},{}]".format(LimPred,MyLim))

            else:
                succSocket1 = context.socket(zmq.PAIR)
                succSocket1.connect("tcp://"+hostsucc+":" + portsucc)
                succSocket1.send_json({'op': 'new', 'key': key, 'key1': myhost, 'key2': porhost,'key3': hostsucc, 'key4': portsucc})
                succSocket1.close()


        elif m['op'] == 'upsucc':
            LimPred = m['key']
            hostsucc=m['key1']
            portsucc=m['key2']
            limsucc= hashlib.sha256(m['key1'].encode('utf-8')).hexdigest()
            print("\nNuevo Rango ({},{}]".format(LimPred,MyLim))

        elif m['op'] == 'uppred':
            hostpre=m['key1']
            portpre=m['key2']
            limpred= m['key1']
            print("\nNuevo Rango ({},{}]".format(LimPred,MyLim))


        else:
            OperacionesToquens(m, MyLim, LimPred)
            


    if clientSocket in socks and socks[clientSocket] == zmq.POLLIN:
        m = clientSocket.recv_json()
        OperacionesToquens(m, MyLim, LimPred)