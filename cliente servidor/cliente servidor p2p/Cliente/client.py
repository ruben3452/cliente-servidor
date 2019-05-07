import zmq
import sys
from threading import Thread
from queue import Queue
import pygame
import math
import base64
import json
import hashlib

pygame.init()

def playerThread(playList, server):
    while True:
        print("PlayerThread iteration")
        songName = playList.get()
        print("Need to handle {}".format(songName))
        # Download the song
        server.send_json({"operacion": "descarga", "cancion":songName})
        musicaOgg = server.recv()
        print("File received")
        # Write the song to file
        with open("down-" + songName, "wb") as archivoOgg:
            archivoOgg.write(musicaOgg)
        print("File saved")
        # Play the song
        pygame.mixer.music.load("down-" + songName)
        pygame.mixer.music.play()
        # wait until the song finishes to play
        while pygame.mixer.music.get_busy():
            pass
        print("File played")

def main():

    # Create the socket and the context
    context = zmq.Context()

    s1 = context.socket(zmq.PAIR)
    s1.connect("tcp://localhost:5555")

    s2 = context.socket(zmq.PAIR)
    s2.connect("tcp://localhost:7777")
  

    while True :
        print ('MENU')
        print ('1.upload')
        print ('2.Download')
                
        print ("respuesta: ")
        command = sys.stdin.readline()
        options = command.split()
        operacion = options[0]
        
        #operacion para listar archivos
        if operacion == "4":
            s.send_json({"operacion": "lista"})
            respuesta = s.recv_json()
            print("Disponibles:")
            for c in respuesta["canciones"]:
                print("\t{0}.{1}".format(g + 1,c))

        #operacion para adicionar
        elif operacion == "1":

            #Envia Operaciones
            s1.send_json({"operacion": "adicionar"})
            s2.send_json({"operacion": "adicionar"})
            
            print ("Nombre Del Archivo")
            command = sys.stdin.readline()
            options = command.split()
            fileName = options[0]
            
            #Envia Nombre
            s1.send_string(fileName)
            s2.send_string(fileName)

            with open(fileName,"rb") as input:
                data = input.read(1024*1024)
                parts = int(len(data)/(1024*1024))

                #Envia El Numero De Partes
                s1.send_string(str( math.ceil(parts/2)))
                s2.send_string(str(math.floor(parts/2)))
                
                i = 0
                server = 1

                toquen_prin = hashlib.sha256(data).hexdigest()
                Arch_str=""
                pri=0

                base64_bytes = base64.b64encode(data)
                base64_string = base64_bytes.decode('utf-8')
                
                while(i<round(int(parts))):
                    input.seek((1024*1024)*i)
                    data = input.read(1024*1024)

                    if i<parts:
                        parts_base64_string = base64_string[(1048576*i):]
                    else:
                        parts_base64_string = base64_string[(1048576*i):(1048576*(i+1))]
                    
                    #print(base64_string)

                    toquen = hashlib.sha256(data).hexdigest()
                    raw_data = {'toquen': toquen, 'datos': parts_base64_string}
                    #Construccion De Indice
                    if pri==0:
                        Arch_str=toquen
                        pri=1
                    else:
                        Arch_str=Arch_str+","+toquen

                    #mirar a que servidor se debe enviar
                    if(server==1):
                    	s1.send_json(raw_data)
                    	server=0
                    else:
                    	s2.send_json(raw_data)
                    	server=1

                    i = i + 1

                #Envia Indices A Los Servidores
                ext = fileName.split(".")
                Arch={"toquen": toquen_prin,"partes":Arch_str,"ext": ext[1]}
                s1.send_json(Arch)
                s2.send_json(Arch)

                print ("Toquen: "+ toquen_prin)

        #operacion para descargar
        elif operacion == "2":

            s1.send_json({"operacion": "descarga"})

            #Recibe Indice Por Consola
            print ("Indice: ")
            command = sys.stdin.readline()
            options = command.split()
            indice = options[0]
            
            #Envia Indice
            s1.send_string(indice)

            #Recibe Toquens De partes
            indi = s1.recv_json()
            Indices = indi["Indices"]
            Indices=Indices.split(",")
            ext=indi["ext"]

            i = 0
            server = 1
            file= ""

            while(i<len(Indices)):
                if(server==1):
                    s1.send_json({"operacion": "completa"})
                    s1.send_string(Indices[i])
                    arch = s1.recv_json()
                    file = file+arch["completa"]
                    server=0
                    
                else:
                    s2.send_json({"operacion": "completa"})
                    s2.send_string(Indices[i])
                    arch = s2.recv_json()
                    file = file+arch["completa"]
                    server=1
                    
                i=i+1

            #print (file)
            print ("Nombre Archivo: ")
            command = sys.stdin.readline()
            options = command.split()
            filedown = options[0]
            

            fbytes = base64.b64decode(file)
            with open(filedown+"."+ext, 'wb') as output:
                    output.write(fbytes)
            print("Descarga Completa")

            

        else:
            print("No esta implementado")



if __name__ == '__main__':
    main()