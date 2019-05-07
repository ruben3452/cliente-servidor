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

    context = zmq.Context()#crea el contesto para la comunicacion
    print ("IP Del Server A Conectar: ")#me imprime en pantalla que le ingrese la ip del nodo ue me voy a conectar
    command = sys.stdin.readline()#me lee lo que le ingrese por teclado de la ip que me solisito
    ipserver = command.split()#me guarda esa informacion que le ingrese en una variable 
    ipser = ipserver[0]#me guarda la informacion en una posicion 
    s1 = context.socket(zmq.PAIR)#aca hago la creacion del soket para poder comunicarme con los servidores 
    s1.connect("tcp://"+ipser+":7772")#aca es donde hago la coneccion y establesco el puerto por donde me voy a comunicar

    myhost = "192.168.0.17"#aca es donde asigno un  a variable con mi ip con el objetivo de cuando necesite descargar el nodo responsable resiba mi ip y mi puerto para que aya comunicacion
    myport = "10001"#aca asigno el puerto para la comun icacion en la descarga
    mySocket = context.socket(zmq.PAIR)#crea un nuevo soquet encargado de la descarga por medio de este es nla comunicacion
    mySocket.bind("tcp://*:"+ myport )#bind crea el soket como servidor para la descarga


    while True :# aca inicializamos el ciclo para ejecutar el menu

        print ('MENU')
        print ('1.upload')
        print ('2.Download')
                
        print ("respuesta: ")
        command = sys.stdin.readline()#aca me lee el valor que le ingrese por teclado 
        options = command.split()#aca es donde me guarda y me separa 
        operacion = options[0]#aca es donde me le asigna una posicion
        
        #operacion para adicionar
        if operacion == "1":#aca agregamos si es la opcion uno pues empieza con la operacion de subida

            print ("Nombre Del Archivo")#imprime en pantalla que ingresemos el nombre del archivo que vamos a subir
            command = sys.stdin.readline()#aca me lee lo mque le ingresamos
            options = command.split()#aca me separa y me guarda lo que leyo
            fileName = options[0]#aca me posesiona lo que leyo

            if path.exists(fileName):#mira si existe el archivo o no para poder seguir
                print ("Por Favor Espere(Puede Tardar Unos Minutos)")#imprime que la operacion para empesar a descargar puede tardar

                partes= math.ceil(os.path.getsize(fileName)/1048576)#aca me lee el total del archivo y me lo divide en 1 mega y me le aplica lo de la aproximacion al mayor

                h = hashlib.sha256()#aca me empieza a implemartar el toquen principal 
                with open(fileName, 'rb',buffering=0) as a:#me habre el archivo y me lo empiesas a leer por bais
                    for b in iter(lambda: a.read(1024*1024), b''):#aca me lee en bais y me dice que me lo lea por megas 
                        h.update(b)#aca en este pedaso lo que hace es que no me lo lee todo en memoria si no que me lo va partiendo y me lo va guardando
                    toquen_prin = h.hexdigest()#aca me va uniendo las partes que lei en memoria para consolidar un solo archivo en un solo toquen principal

                pri=0#inicialiso en cero a pri
                i = 0#i es igual a cero 
                while(i<partes):#empieso a hacer un ciclo 
                    time.sleep(0.1)#se implemento para que la comunicacion no se perdiera
                    with open(fileName, 'rb') as archivo:#abre el archivo y me lo lee en bait 

                        archivo.seek(i*1048576)#aca me va asignando las partes y me las va colocando en orden con el sikk
                        contet = archivo.read(1048576)#voy leyendo el archivo por cada mega y lo guardo en una variable
                        base64_bytes = base64.b64encode(contet)#aca me codifica el archivo en baits 
                        base64_string = base64_bytes.decode('utf-8')#aca me lo decodifica en string 

                    toquen = hashlib.sha256(base64_string.encode('utf-8')).hexdigest()#aca crea el toquen para cada parte 
                    raw_data = {'op':'adicionar','toquen': toquen, 'datos': base64_string}# aca lo que hace es que me crea el json 
                    s1.send_json(raw_data)#envia ese json de cada una de las partes 

                    #Construccion De Indice
                    if pri==0:
                        Arch_str=toquen#aca es donde guarda los toquen pequeños en la variable arch_str
                        pri=1
                    else:
                        Arch_str=Arch_str+","+toquen#si no que me ponga otro toquen separado de una coma

                    i=i+1
                    

                file = fileName.split(".")#aca lo que hace es que me coge el nombre y me lo separa con un punto paa ponerle la extencion
                archi_prin={"toquen":toquen_prin,"partes":Arch_str,"ext": file[1]}#en la varible me guarda el toquen principal con sus partes y la extencion del archivo 
                json_data = json.dumps(archi_prin, indent=2)#aca ya me crea el torren por asi decirlo

                with open(file[0]+"_down.json", 'w') as output:#me abre el nombre del archivo y lo escribe 
                    output.write(json_data)#dudaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

                print("Archivo Subido")#me imprime que el archivo a sido subido

            else:
                print("Archivo NO Existe")#me dice que no encontro el archivo que no existe

        
        elif operacion == "2":#si la operacion es dos entonces inicia el procesos de cargar

            print ("Cargar Archivo: ")#me pide el nombre del archivo que se quiere descargar
            command = sys.stdin.readline()#me lee lo que le ingrese por teclado
            options = command.split()#aca me lo separa con su extencion 
            File = options[0]#aca me lo poseciona 
            
            if path.exists(File):#si el archivo existe entonces empieza 

                with open(File, 'r') as input:#me abre el archivo en lectura 
                    new_json_data = json.load(input)#aca en esta variable me carga este archivo con el lleisom 
                    Indices = new_json_data["partes"]#aca ya me empiesa a construir todas las partes que se van a descargar
                    Indices=Indices.split(",")#aca me empieza a separar cada una de las partes 
                    ext = new_json_data["ext"]#aca me le agrega la extencion a ese archivo que se va a descargar 

                print ("Nombre Archivo(Para Descarga): ")#aca le meto el npmbre que quiro para mi archivo
                command = sys.stdin.readline()#me lee lo que le ingrese por teclado
                options = command.split()#aca me lo separa con su extencion 
                filedown = options[0]#aca me lo poseciona 

                print ("Por Favor Espere(Puede Tardar Unos Minutos)")

                with open(filedown+"."+ext, 'wb') as output:#lo que le ingrese por teclado me lo abre por escritura y me dice que me lo separe el  nombre con la extencion
                    i = 0
                    file= ""
                    while(i<len(Indices)):#aca empieza el siclo para leer el indice 
                        time.sleep(0.1)
                        s1.send_json({"op": "completa","indice":Indices[i],"myhost":myhost,"myport":myport})#aca me dice que necesito ese indice y que mi ip y mi puerto es tal
                        arch = mySocket.recv_json()#aca me empiesa a resivir lo que el noodo me manda  
                        file = arch["completa"]#ese ya me lo nombra cuando se completa la descarga

                        output.seek(i*1048576)#aca es donde me coge ya tosos los archivos en string y empieza a decodificar a bais
                        fbytes = base64.b64decode(file)#aca me empiesa a combertir en baits
                        output.write(fbytes)#aca me los escribe en bais  

                        i=i+1

                print("Descarga Completa")

            else:
                
                print("Archivo NO Existe")
            

        else:
            print("Opcion No esta implementado")



if __name__ == '__main__':
    main()
