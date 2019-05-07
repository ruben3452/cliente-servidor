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

    while True:
        command = sys.stdin.readline()
        options = command.split()
        operacion = options[0]
        if operacion == "lista":
            s.send_json({"operacion": "lista"})
            respuesta = s.recv_json()
            print("Canciones disponibles:")
            for c in respuesta["canciones"]:
                print("\t{}".format(c))
        elif operacion == "adicionar":
            cancion = options[1]
            playList.put(cancion)
        elif operacion == "reproducir":
            cancion = options[1]
            s.send_json({"operacion": "descarga", "cancion":cancion})
            musicaOgg = s.recv()
            # musicaOgg contiene la cancion que se va a reproducir
            with open("down-" + cancion, "wb") as archivoOgg:
                archivoOgg.write(musicaOgg)
            # Reproducir la musica
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.queue("down-" + cancion)
            else:
                pygame.mixer.music.load("down-" + cancion)
                pygame.mixer.music.play()
        elif operacion == "pausa":
            pygame.mixer.music.pause()
        elif operacion == "seguir":
            pygame.mixer.music.unpause()
        else:
            print("No esta implementado")

if __name__ == '__main__':
    main()
