import os
import sys
import zmq
import base64
import json


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

    # Create the socket and the context
    context = zmq.Context()
    s = context.socket(zmq.PAIR)
    s.bind("tcp://*:5555")

    print ("Se Inicio El Servidor 1")

    while True:
        msg = s.recv_json()


        if msg["operacion"] == "lista":
            s.send_json({"canciones": list(files.keys())})

        #Operacion para adicionar
        elif msg["operacion"] == "adicionar":

            #Recibe Nombre
            fileName= s.recv_string()          

            #Recibe Numero De Partes
            parts = s.recv_string()

            print ("Se va A Recibir El Archivo: " + fileName)

            i=0

            
            while(i<round(int(parts))):
                File = s.recv_json()
                
                archi={File["toquen"]:File["datos"]}

                json_data = json.dumps(archi, indent=1)

                with open("toquen/"+File["toquen"]+".json", 'w') as output:
                    output.write(json_data)

                i = i + 1

            print ("resivido la parte: " + parts)

            indi = s.recv_json()
            archi_prin={indi["toquen"]:indi["partes"],"ext":indi["ext"]}
            json_data = json.dumps(archi_prin, indent=2)

            with open("principales/"+indi["toquen"]+".json", 'w') as output:
                output.write(json_data)


            

        elif msg["operacion"] == "descarga":

            #Recibe indice
            indice= s.recv_string()
            print ("Se va A Descargar El Indice: " + indice)

            with open("principales/"+indice+".json", 'r') as input:
                new_json_data = json.load(input)
                fstring = new_json_data[indice]
                extstring = new_json_data["ext"]
                
            s.send_json({"Indices": fstring,"ext": extstring})
            

        elif msg["operacion"] == "completa":

            #Recibe indice
            indice= s.recv_string()

        
            with open("toquen/"+indice+".json", 'r') as input:
                new_json_data = json.load(input)
                fstring = new_json_data[indice]
            
            s.send_json({ "completa": fstring })

            print("descarga terminada")
            
                        


if __name__ == '__main__':
    main()
