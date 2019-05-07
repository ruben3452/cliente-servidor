import os
import sys
import zmq

def loadFiles(path):
    files = {}
    dataDir = os.fsencode(path)
    for file in os.listdir(dataDir):
        filename = os.fsdecode(file)
        print("Loading {}".format(filename))
        files[filename] = file
    return files

def readPart(fileName, part):
    with open(fileName,"rb") as input:
        input.seek(1024*part)
        data = input.read(1024)
    #for i in range(part):
     #   input.seek(1024*i)
      #  data = input.read(1024)
                #     s.send(data)
                #     s.recv_string()   
        return data


def main():
    musicFolder = sys.argv[1]
    print("Serving files from {}".format(musicFolder))
    files = loadFiles(musicFolder)
    print("Load info on {} files.".format(len(files)))

    # Create the socket and the context
    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind("tcp://*:5555")

    while True:
        msg = s.recv_json()
        if msg["operacion"] == "lista":
            s.send_json({"canciones": list(files.keys())})
        elif msg["operacion"] == "descarga":
            fileName = musicFolder + msg["cancion"]
            with open(fileName,"rb") as input:
                data = input.read()
                sizeMBytes = len(data) / 1024/1024
                print("Size in MB {}".format(sizeMBytes))
                parts = int(len(data)/1024)
                s.send_string(str(parts))
                msg = s.recv_string()
                print ("Recibido partes" + msg)
                #s.send(data)

                i = 0
                while(i<round(int(parts))):
                    input.seek(1024*i)
                    data = input.read(1024)
                    s.send(data)
                    s.recv_string()
                    i = i + 1

                 # for i in range(parts):
                 #     input.seek(1024*i)
                 #     data = input.read(1024)
                 #     s.send(data)
                 #     s.recv_string()
                 # print("Termina envio")
        
            #     print("solicitud recibida ")
            #     fileName = musicFolder 

            #     data = readPart(fileName, parts)
            if i == parts:
                 s.send_string("fish")
                 s.recv_string()
                 msg = s.recv_json()
            else:
                s.send_string("t")
        



if __name__ == '__main__':
    main()