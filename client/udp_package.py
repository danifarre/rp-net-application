from struct import *

# Paquetes
REG_REQ = 'REG_REQ'
REG_INFO = 'REG_INFO'
REG_ACK = 'REG_ACK'
INFO_ACK = 'INFO_ACK'
REG_NACK = 'REG_NACK'
INFO_NACK = 'INFO_NACK'
REG_REJ = 'REG_REJ'

# Formato de los paquetes
UDP_FORMAT = '!B13s9s61s'


# Tipo de paquete
type_package = {REG_REQ : 0x00,
                REG_INFO : 0x01,
                REG_ACK : 0x02, 
                INFO_ACK : 0x03, 
                REG_NACK : 0x04, 
                INFO_NACK : 0x05, 
                REG_REJ : 0x06
}

num_package = {0 : REG_REQ,
                1 : REG_INFO,
                2 : REG_ACK,
                3 : INFO_ACK,
                4 : REG_NACK,
                5 : INFO_NACK,
                6: REG_REJ
    
}

class UDPPackage(object):
    def __init__(self):
        self.pack_info = ()

    def pack(self, package, id = '', random = '', data = ''):
        """Empaqueta las entradas, en función del tipo de paquete. 
           Y lo almacena, para poder obtener su información.
        """
        
        result = ''

        if package == REG_REQ:
            result = pack(UDP_FORMAT, type_package[REG_REQ], id.encode(), '00000000'.encode(), ''.encode())
            self.pack_info = (calcsize(UDP_FORMAT), REG_REQ, id, '00000000', '')
        elif package == REG_INFO:
            result = pack(UDP_FORMAT, type_package[REG_INFO], id.encode(), random.encode(), data.encode())
            self.pack_info = (calcsize(UDP_FORMAT), REG_INFO, id, random, data)
        
        return result

    def unpack(self, package):
        """Desempaqueta la entrada, la devuelbe como una tupla
           Y lo almacena, para poder obtener su información.
        """
        result = {}
        data = unpack(UDP_FORMAT, package)

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
        for c in data[3].decode("utf-8", errors="replace"):
            if c == "\x00":
                break
            aux = aux + c
        result['data'] = aux

        self.pack_info = (calcsize(UDP_FORMAT), result['type'], result['id'], result['random'], result['data'])
        
        return result


    def get_last_package(self):
        """Devuelbeuna tupla con la información del último paquete empaquetado/desempaquetado
           Formato: (tamaño, nombre, identificador, random, datos)
        """

        return self.pack_info

    def get_package_format(self, name):
        pack_format = {}
        if name == REG_ACK:
            pack_format['type'] = REG_ACK
            pack_format['id'] = ''
            pack_format['rndm'] = ''
            pack_format['data'] = ''

        return pack_format