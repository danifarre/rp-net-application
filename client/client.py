#!/usr/bin/env python

import sys, optparse, time
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

MAX_REGISTRATION_ATTEMPTS = 3

# Etiquetas para calcular tiempos de envio/recepción de paquete de registro
T,  U,  N,  O,  P,  Q  = 1, 2, 7, 3, 3, 3

class Client(object):

    def __init__(self, configuration, debug):
        self.state = states.States()
        self.udp_package = udp_package.UDPPackage()
        self.configuration = configuration
        self.debug = client_debug.Debug()
        self.server_info = {}
        self.registration_attempts = 0

    def run(self):
        """Arranca el client
        """

        self.debug.start_loop_service(configuration['Id'])
        if not self.registry():
            sys.exit(1)

    def registry(self):
        self.state_not_registered()

    def state_not_registered(self):
        global pack, udp_sock
        self.registration_attempts += 1

        if self.registration_attempts > MAX_REGISTRATION_ATTEMPTS:
            self.debug.could_not_register(MAX_REGISTRATION_ATTEMPTS)
            return False

        # Passem al estat NOT_REGISTERED
        self.state.to_not_registered()
        self.debug.new_registration_process(self.state.get_actual_state(), self.registration_attempts)

        # Instanciem el socket en mode UDP
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Creem el paquet REG_REG, i l'enciem al servidor
        pack = self.udp_package.pack(REG_REQ, configuration['Id'])
        udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
        self.debug.send_udp_package(self.udp_package.get_last_package())

        return self.state_wait_ack_reg()

    def state_wait_ack_reg(self):
        global pack, udp_sock

        # El client passa a l'estat WAIT_ACK_REG
        self.state.to_wait_ack_reg()
        self.debug.state_change(self.state.get_actual_state())

        # Esperamos la respuesta del servidor
        answer = self.__wait_reg_req_response(T, U, N - 1, O, P - 1, Q)

        # Si no obtenemos respuesta, el cliente termina
        if answer == None:
            time.sleep(U)
            return self.state_not_registered()

        # Desempaquetamos la entrada, y analizamos el paquete
        unpacked = self.udp_package.unpack(answer)
        self.debug.received_udp_package(self.udp_package.get_last_package())

        if unpacked['type'] == REG_NACK:
            self.debug.discarded_package_with_reason(unpacked['data'])

            self.state.to_not_registered()
            self.debug.state_change(self.state.get_actual_state())

            # Creem el paquet REG_REG, i l'enciem al servidor
            pack = self.udp_package.pack(REG_REQ, configuration['Id'])
            udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

            return self.state_wait_ack_reg()

            if unpacked == None:
                return state_not_registered()

        elif unpacked['type'] == REG_ACK:
            self.server_info['id'] = unpacked['id']
            self.server_info['random'] = unpacked['random']
            self.server_info['server-udp'] = unpacked['data']

            pack = self.udp_package.pack(REG_INFO,
                                         configuration['Id'],
                                         self.server_info['random'],
                                         configuration['Server-UDP'] + ',' + configuration['Params'])


            udp_sock.sendto(pack, (self.configuration['Server'], int(self.server_info['server-udp'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

            return self.state_wait_ack_info()

        elif unpacked['type'] == REG_REJ:
            self.debug.package_rejected_with_reason(unpacked['data'])
            return self.state_not_registered() 

    def state_wait_ack_info(self):
        """Estat WAIT_ACK_REG
        """

        global pack, udp_package

        self.state.to_wait_ack_info()
        self.debug.state_change(self.state.get_actual_state())

        try:
            answer = udp_sock.recv(84)
            unpacked = self.udp_package.unpack(answer)
            self.debug.received_udp_package(self.udp_package.get_last_package())
        except socket.timeout:
            return self.state_not_registered()

        if unpacked['type'] == INFO_ACK:
            self.debug.accepted_device()
            return self.state_registered()

        elif unpacked['type'] == INFO_NACK:
            self.debug.discarded_package_with_additional_info(unpacked['data'])

            self.state.to_not_registered()
            self.debug.state_change(self.state.get_actual_state())

            # Creem el paquet REG_REG, i l'enciem al servidor
            pack = self.udp_package.pack(REG_REQ, configuration['Id'])
            udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

            return self.state_wait_ack_reg(pack)

            if unpacked == None:
                return state_not_registered()

    def state_registered(self):
        self.state.to_registered()
        self.debug.state_change(self.state.get_actual_state())   

    def __wait_reg_req_response(self, t, u, n, o, p, q):
        global udp_sock

        answer = None
        udp_sock.settimeout(t)

        while p > 0:
            n -= 1
            try:
                answer = udp_sock.recv(84)
                if answer != None:
                    return answer
            except socket.timeout:
                p -= 1
            udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

        t += 1
        while t < T * q:
            udp_sock.settimeout(t)
            n -= 1
            try:
                answer = udp_sock.recv(84)
                if answer != None:
                    return answer
            except socket.timeout:
                t += 1
            udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

        while n > 0:
            udp_sock.settimeout(t)
            n -= 1
            try:
                answer = udp_sock.recv(84)
                if answer != None:
                    return answer
            except socket.timeout:
                pass
            udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

        try:
            answer = udp_sock.recv(84)
            if answer != None:
                return answer
        except socket.timeout:
            pass

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