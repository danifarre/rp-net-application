from struct import *

# Paquetes
SEND_DATA = 'SEND_DATA'
SET_DATA = 'SET_DATA'
GET_DATA = 'GET_DATA'
DATA_ACK = 'DATA_ACK'
DATA_NACK = 'DATA_NACK'
DATA_REJ = 'DATA_REJ'


# Formato de los paquetes
TCP_FORMAT = '!B13s9s8s16s80s'


# Tipo de paquete
type_package = {SEND_DATA : 0x20,
                SET_DATA : 0x21,
                GET_DATA : 0x22, 
                DATA_ACK : 0x23, 
                DATA_NACK : 0x24, 
                DATA_REJ : 0x25, 
}

num_package = { 32 : SEND_DATA,
                33 : SET_DATA,
                34 : GET_DATA,
                35 : DATA_ACK,
                36 : DATA_NACK,
                37 : DATA_REJ,
}

class TCPPackage(object):
    def __init__(self):
        self.pack_info = ()

    def pack(self, package, id = '', random = '00000000', element = '', valor = '', info = ''):
        """Empaqueta las entradas, en función del tipo de paquete. 
           Y lo almacena, para poder obtener su información.
        """
        
        result = ''

        result = pack(TCP_FORMAT, type_package[package], id.encode(), random.encode(), element.encode(), valor.encode(), info.encode())
        self.pack_info = (calcsize(TCP_FORMAT), package, id, random, element, valor, info)

        return result

    def unpack(self, package):
        """Desempaqueta la entrada, la devuelbe como una tupla
           Y lo almacena, para poder obtener su información.
        """
        result = {}
        data = unpack(TCP_FORMAT, package)

        result['type'] = num_package[data[0]]

        aux = ''
        for c in data[1].decode():
            if c == "\x00":
                break
            aux = aux + c
        result['id'] = aux

        aux = ''
        for c in data[2].decode():
            if c == "\x00":
                break
            aux = aux + c
        result['random'] = aux

        aux = ''
        for c in data[3].decode():
            if c == "\x00":
                break
            aux = aux + c
        result['element'] = aux

        aux = ''
        for c in data[4].decode("utf-8", errors="replace"):
            if c == "\x00":
                break
            aux = aux + c
        result['valor'] = aux

        aux = ''
        for c in data[5].decode("utf-8", errors="replace"):
            if c == "\x00":
                break
            aux = aux + c
        result['info'] = aux

        self.pack_info = (calcsize(TCP_FORMAT), result['type'], result['id'], result['random'], result['element'], result['valor'], result['info'])
        
        return result


    def get_last_package(self):
        """Devuelbeuna tupla con la información del último paquete empaquetado/desempaquetado
           Formato: (tamaño, nombre, identificador, random, datos)
        """

        return self.pack_info