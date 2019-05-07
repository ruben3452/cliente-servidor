import zmq
import sys
from threading import Thread
from queue import Queue
import pygame

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
    s = context.socket(zmq.REQ)
    s.connect("tcp://localhost:5555")

    playList = Queue()
    player = Thread(target=playerThread, args=(playList,s))
    player.start()

    while True :
        print ('MENU')
        print ('1.Lista')
        print ('2.upload')
        print ('3.Download')
        print ('4.')
        
        print ("respuesta: ")
        command = sys.stdin.readline()
        options = command.split()
        operacion = options[0]
        
        #operacion para listar archivos
        if operacion == "1":
            s.send_json({"operacion": "lista"})
            respuesta = s.recv_json()
            print("Canciones disponibles:")
            for c in respuesta["canciones"]:
                print("\t{0}.{1}".format(g + 1,c))

        #operacion para adicionar
        elif operacion == "2":
            s.send_json({"operacion": "adicionar"})

            resp = s.recv_string()

            print ("Nombre Del Archivo")
            command = sys.stdin.readline()
            options = command.split()
            fileName = options[0]
            
            #Envia Nombre
            s.send_string(fileName)
            resp = s.recv_string()

            with open(fileName,"rb") as input:
                data = input.read()
                sizeMBytes = len(data) / 1024/1024
                parts = int(len(data)/1024)
                s.send_string(str(parts))
                msg = s.recv_string()

                i = 0
                while(i<round(int(parts))):
                    input.seek(1024*i)
                    data = input.read(1024)
                    #mirar a que servidor se debe enviar
                    s.send(data)
                    s.recv_string()
                    i = i + 1
            
        #operacion para descargar
        elif operacion == "3":

            s.send_json({"operacion": "descarga"})
            resp = s.recv_string()

            #Recibe Nombre
            print ("Nombre Del Archivo")
            command = sys.stdin.readline()
            options = command.split()
            cancion = options[0]
            
            #Envia Nombre
            s.send_string(cancion)


            parts = s.recv_string()
            s.send_string("Recibido")
            
            fileSong = open("down-"+cancion, "wb") 
            fileSong.close()

            with open("down-"+cancion, "ab") as archivoOgg:
                i = 0
                while(i<round(int(parts))):
                    musicaOgg = s.recv()
                    archivoOgg.write(musicaOgg)
                    s.send_string("OK")
                    i = i + 1
                print (i)


        else:
            print("No esta implementado")



if __name__ == '__main__':
    main()