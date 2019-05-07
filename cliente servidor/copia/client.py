import zmq
import sys
from threading import Thread
from queue import Queue
import math 
import base64
import json
import hashlib
import os
import os.path as path
from os import listdir
import time

def main():

    context = zmq.Context() 
    print ("IP Del Server A Conectar: ")
    command = sys.stdin.readline()
    ipserver = command.split()
    ipser = ipserver[0]
    s1 = context.socket(zmq.PAIR)
    s1.connect("tcp://"+ipser+":7772")

    myhost = "192.168.0.50"
    myport = "10001"
    mySocket = context.socket(zmq.PAIR)
    mySocket.bind("tcp://*:"+ myport )


    while True :

        print ('MENU')
        print ('1.upload')
        print ('2.Download')
                
        print ("respuesta: ")
        command = sys.stdin.readline()
        options = command.split()
        operacion = options[0]
        
        #operacion para adicionar
        if operacion == "1":

            print ("Nombre Del Archivo")
            command = sys.stdin.readline()
            options = command.split()
            fileName = options[0]

            if path.exists(fileName):
                print ("Por Favor Espere(Puede Tardar Unos Minutos)")

                partes= math.ceil(os.path.getsize(fileName)/1048576)

                h = hashlib.sha256()
                with open(fileName, 'rb',buffering=0) as a:
                    for b in iter(lambda: a.read(1024*1024), b''):
                        h.update(b)
                    toquen_prin = h.hexdigest()

                pri=0
                i = 0
                while(i<partes):
                    time.sleep(0.5)
                    with open(fileName, 'rb') as archivo:

                        archivo.seek(i*1048576)
                        contet = archivo.read(1048576)
                        base64_bytes = base64.b64encode(contet)
                        base64_string = base64_bytes.decode('utf-8')

                    toquen = hashlib.sha256(base64_string.encode('utf-8')).hexdigest()
                    raw_data = {'op':'adicionar','toquen': toquen, 'datos': base64_string}
                    s1.send_json(raw_data)

                    #Construccion De Indice
                    if pri==0:
                        Arch_str=toquen
                        pri=1
                    else:
                        Arch_str=Arch_str+","+toquen

                    i=i+1
                    

                file = fileName.split(".")
                archi_prin={"toquen":toquen_prin,"partes":Arch_str,"ext": file[1]}
                json_data = json.dumps(archi_prin, indent=2)

                with open(file[0]+"_down.json", 'w') as output:
                    output.write(json_data)

                print("Archivo Subido")

            else:
                print("Archivo NO Existe")

        
        elif operacion == "2":

            print ("Cargar Archivo: ")
            command = sys.stdin.readline()
            options = command.split()
            File = options[0]
            
            if path.exists(File):

                with open(File, 'r') as input:
                    new_json_data = json.load(input)
                    Indices = new_json_data["partes"]
                    Indices=Indices.split(",")
                    ext = new_json_data["ext"]

                print ("Nombre Archivo(Para Descarga): ")
                command = sys.stdin.readline()
                options = command.split()
                filedown = options[0]

                print ("Por Favor Espere(Puede Tardar Unos Minutos)")

                with open(filedown+"."+ext, 'wb') as output:
                    i = 0
                    file= ""
                    while(i<len(Indices)):
                        time.sleep(0.5)
                        s1.send_json({"op": "completa","indice":Indices[i],"myhost":myhost,"myport":myport})
                        arch = mySocket.recv_json()
                        file = arch["completa"]

                        output.seek(i*1048576)
                        fbytes = base64.b64decode(file)
                        output.write(fbytes)

                        i=i+1

                print("Descarga Completa")

            else:
                
                print("Archivo NO Existe")
            

        else:
            print("Opcion No esta implementado")



if __name__ == '__main__':
    main()
