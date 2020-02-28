#!/usr/bin/env python

import sys, optparse
import socket
import time
import states, udp_package

# Paquetes
REG_REQ = 'REG_REQ'
REG_INFO = 'REG_INFO'
REG_ACK = 'REG_ACK'
INFO_ACK = 'INFO_ACK'
REG_NACK = 'REG_NACK'
INFO_NACK = 'INFO_NACK'
REG_REJ = 'REG_REJ'

# Etiquetas para calcular tiempos de envio/recepción de paquete de registro
T,  U,  N,  O,  P,  Q  = 1, 2, 7, 3, 3, 3

class Client(object):

    def __init__(self, configuration, debug):
        self.state = states.States()
        self.udp_package = udp_package.UDPPackage()
        self.configuration = configuration
        self.debug = debug

    def run(self):
        """Arranca el cliente
        """

        self.registry()

    def registry(self):
        """Registra el cliente con el servidor
        """

        # Instanciamos el socket de tipo UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Creamos el paquete REG_REG y lo enviamos al servidor
        pack = self.udp_package.pack(REG_REQ, configuration['Id'])
        sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))

        # El cliente pasa al estado WAIT_ACK_REG
        self.state.to_wait_ack_reg()

        # Esperamos la respuesta del servidor
        answer = wait_registration_response(self, sock, T, U, N, O, P, Q)

        #Si no obtenemos respuesta, el cliente termina
        if answer == None:
            sys.exit(1)

        pack = self.udp_package.unpack(answer)

        start = time.time()
        final = time.time()
        elapsed_time = round(final - start, 0)

def wait_registration_response(self, sock, t, u, n, o, p, q):
    answer = None
    while o > 0:
        while p > 0:
            sock.settimeout(t)
            n -= 1
            try:
                answer = sock.recv(84)
                if answer != None:
                    return answer
            except socket.timeout:
                p -= 1
                t += 1
        while t < T * q:
            sock.settimeout(t)
            n -= 1
            try:
                answer = sock.recv(84)
                if answer != None:
                    return answer
            except socket.timeout:
                t += 1

        while n > 0:
            sock.settimeout(t)
            n -= 1
            try:
                answer = sock.recv(84)
                if answer != None:
                    return answer
            except socket.timeout:
                pass
        o -= 1
    return answer

def read_configuration(file_name):
    """Almacena la configuración del cliente, leyendo el fichero por defecto, o introducido por parametro
    """

    configuration = {}

    with open(file_name) as f:
        for line in f:
            configuration[line[: line.index('=') - 1]] = line[line.index('=') + 2: -1]

    return configuration


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-c', '--configuration', action='store', type='string', default='client.cfg', help='File of configurations')
    parser.add_option('-d', '--debug', action='store_true', default='false', help='Debuging?')
    (options, args) = parser.parse_args()

    configuration = read_configuration(options.configuration)

    client = Client(configuration, options.debug)

    client.run()