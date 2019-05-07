import zmq
import sys
import pygame

pygame.init()

def main():
    # Create the socket and the context
    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect("tcp://localhost:5555")

    operacion = sys.argv[1]
    if operacion == "lista":
        s.send_json({"operacion": "lista"})
        respuesta = s.recv_json()
        print("Canciones disponibles:")
        for c in respuesta["canciones"]:
            print("\t{}".format(c))
    elif operacion == "reproducir":
        cancion = sys.argv[2]
        s.send_json({"operacion": "descarga", "cancion":cancion})
        musicaOgg = s.recv()
        # musicaOgg contiene la cancion que se va a reproducir
        with open("descarga.ogg", "wb") as archivoOgg:
            archivoOgg.write(musicaOgg)
        # Reproducir la musica
        song = pygame.mixer.Sound('descarga.ogg')
        song.play()
        #while True:
        #    pass
        print("Todo listo")

    else:
        print("No esta implementado")










if __name__ == '__main__':
    main()