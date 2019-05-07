import socket, random as rn

mappers = [["localhost","4444"],["localhost","4445"],["localhost","4446"]]
reducers = [["localhost","5555"],["localhost","5556"],["localhost","5557"]]
simbolList0 = [95, 65, 97, 66, 98, 67, 99, 68, 100, 69, 101, 70, 102, 71, 103, 72, 104, 73]
simbolList1 = [105, 74, 106,75, 107, 76, 108, 77, 109, 78, 110, 79, 111, 80, 112, 81, 113]
simbolList2 = [82, 114, 83, 115, 84, 116, 85, 117, 86, 118, 87, 119, 88, 120, 89, 121, 90, 122]

cantidadMappers = 3
cantidadReducers = 3

def buscarPuerto(socket,my_port):
    while True:
        mi_puerto = str(my_port)
        try:
            socket.bind("tcp://*:" + mi_puerto)
            return mi_puerto
        except:
            my_port+=1
    return mi_puerto


def buscarIP(argv):
    ip="localhost"
    if len(argv) > 1:
        ip=argv[1]
    return ip

def conectarIP(activo=False):
    if activo:
        return socket.gethostbyname(gethostname())
    else:
        return rn.randint(0,100)
