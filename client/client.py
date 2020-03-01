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

    def run(self):
        """Arranca el cliente
        """
        self.debug.start_loop_service(configuration['Id'])
        self.registry()

    def registry(self):
        """Registra el cliente con el servidor
        """
        registration_attempts = 0

        while registration_attempts < MAX_REGISTRATION_ATTEMPTS:
            self.state.to_not_registered()
            self.debug.new_registration_process(self.state.get_actual_state(), registration_attempts + 1)


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
            answer = self.__wait_reg_req_response(sock, pack, T, U, N - 1, O, P - 1, Q)

            # Si no obtenemos respuesta, el cliente termina
            if answer == None:
                registration_attempts += 1
                time.sleep(U)
                continue

            # Desempaquetamos la entrada, y analizamos el paquete
            unpacked = self.udp_package.unpack(answer)
            self.debug.received_udp_package(self.udp_package.get_last_package())

            # Si el paquete es incorrecto se inicia un nuevo proceso de registrop
            if not self.__valid_package(unpacked):
                registration_attempts += 1
                continue

            if unpacked['type'] == REG_NACK:
                self.debug.discarded_package_with_reason(unpacked['data'])
                unpacked = self.__resend_reg_req(sock)

                if unpacked == None:
                    registration_attempts += 1 
                    continue

            if unpacked['type'] == REG_ACK:
                server_info['id'] = unpacked['id']
                server_info['random'] = unpacked['random']
                server_info['server-udp'] = unpacked['data']

                pack = self.udp_package.pack(REG_INFO,
                                             configuration['Id'],
                                             server_info['random'],
                                             configuration['Server-UDP'] + ',' + configuration['Params'])


                sock.sendto(pack, (self.configuration['Server'], int(server_info['server-udp'])))
                self.debug.send_udp_package(self.udp_package.get_last_package())
                
                self.state.to_wait_ack_info()
                self.debug.state_change(self.state.get_actual_state())

            elif unpacked['type'] == REG_REJ:
                registration_attempts += 1 
                self.debug.package_rejected_with_reason(unpacked['data'])
                self.state.to_not_registered()
                self.debug.state_change(self.state.get_actual_state())
                continue

            answer = sock.recv(84)
            unpacked = self.udp_package.unpack(answer)
            self.debug.received_udp_package(self.udp_package.get_last_package())

            if unpacked['type'] == INFO_NACK:
                self.debug.discarded_package_with_additional_info(unpacked['data'])
                unpacked = self.__resend_reg_req(sock)

                if unpacked == None:
                    registration_attempts += 1 
                    continue

            self.debug.accepted_device()

            self.state.to_registered()
            self.debug.state_change(self.state.get_actual_state())

            break

        else:
            self.debug.could_not_register(MAX_REGISTRATION_ATTEMPTS)
            sys.exit(1)


    def __wait_reg_req_response(self, sock, pack, t, u, n, o, p, q):
        answer = None
        sock.settimeout(t)

        while p > 0:
            n -= 1
            try:
                answer = sock.recv(84)
                if answer != None:
                    return answer
            except socket.timeout:
                p -= 1
            sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

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
            sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

        while n > 0:
            sock.settimeout(t)
            n -= 1
            try:
                answer = sock.recv(84)
                if answer != None:
                    return answer
            except socket.timeout:
                pass
            sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

        try:
            answer = sock.recv(84)
            if answer != None:
                return answer
        except socket.timeout:
            pass

        return answer

    def __resend_reg_req(self, sock):
        while True:
            answer = None

            self.state.to_not_registered()
            self.debug.state_change(self.state.get_actual_state())

            pack = self.udp_package.pack(REG_REQ, configuration['Id'])
            sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

            self.state.to_wait_ack_reg()
            self.debug.state_change(self.state.get_actual_state())

            try:
                answer = sock.recv(84)
                unpacked = self.udp_package.unpack(answer)
                self.debug.received_udp_package(self.udp_package.get_last_package())
            except socket.timeout:
                return None

            if not self.__valid_package(unpacked):
                return None

            if unpacked['type'] == REG_ACK:
                break
            elif unpacked['type'] == REG_NACK:
                self.debug.discarded_package_with_reason(unpacked['data'])
                continue
            elif unpacked['type'] == REG_REJ:
                break
            elif unpacked['type'] == INFO_NACK:
                self.debug.discarded_package_with_additional_info(unpacked['data'])
                continue
        return unpacked

    def __valid_package(self, unpacked):
        return True
        if unpacked['type'] == REG_ACK and self.state.is_wait_ack_reg():
            return True

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