#!/usr/bin/env python

import sys, optparse
import socket
import states, udp_package, client_debug

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
        self.debug = client_debug.Debug()

    def run(self):
        """Arranca el cliente
        """
        self.debug.start_loop_service(configuration['Id'])
        self.state.to_not_registered()
        self.registry()

    def registry(self):
        """Registra el cliente con el servidor
        """

        self.debug.new_registration_process(self.state.get_actual_state())
        while True:
            # Diccionario que usaremos para almacenar el identificador, número aleatorio y la ip del servidor
            server_info = {}

            # Instanciamos el socket de tipo UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Creamos el paquete REG_REG y lo enviamos al servidor
            pack = self.udp_package.pack(REG_REQ, configuration['Id'])
            sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

            # El cliente pasa al estado WAIT_ACK_REG
            self.state.to_wait_ack_reg()
            self.debug.state_change(self.state.get_actual_state())

            # Esperamos la respuesta del servidor
            answer = self.__wait_reg_req_response(sock, T, U, N, O, P, Q)

            # Si no obtenemos respuesta, el cliente termina
            if answer == None:
                continue

            # Desempaquetamos la entrada, y analizamos el paquete
            unpack = self.udp_package.unpack(answer)
            self.debug.received_udp_package(self.udp_package.get_last_package())

            if unpack['type'] == REG_NACK:
                unpack = self.__case_reg_ack(sock, unpack)
                
            if unpack['type'] == REG_ACK:
                server_info['id'] = unpack['id']
                server_info['random'] = unpack['random']
                server_info['server-udp'] = unpack['data']

                pack = self.udp_package.pack(REG_INFO,
                                             configuration['Id'],
                                             server_info['random'],
                                             configuration['Server-UDP'] + ',' + configuration['Params'])


                sock.sendto(pack, (self.configuration['Server'], int(server_info['server-udp'])))
                self.debug.send_udp_package(self.udp_package.get_last_package())
                
                self.state.to_wait_ack_info()
                self.debug.state_change(self.state.get_actual_state())

            elif unpack['type'] == REG_REJ:
                self.state.to_not_registered()
                continue

            answer = sock.recv(84)
            unpack = self.udp_package.unpack(answer)
            self.debug.received_udp_package(self.udp_package.get_last_package())

            self.debug.accepted_device()

            self.state.to_registered()
            self.debug.state_change(self.state.get_actual_state())

            break




    def __wait_reg_req_response(self, sock, t, u, n, o, p, q):
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

    def __case_reg_ack(self, sock, unpack):
        while True:
            answer = None
            if unpack['type'] == REG_ACK:
                break
            elif unpack['type'] == REG_NACK:
                self.state.to_not_registered()
               
                try:
                    answer = sock.recv(84)
                    if answer != None:
                        unpack = answer
                        continue
                except socket.timeout:
                    sys.exit(1)

                self.state.to_wait_ack_reg()
            elif unpack['type'] == REG_REJ:
                break
        return unpack

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