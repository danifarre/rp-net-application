#!/usr/bin/env python

import sys 
import optparse
import time
import threading
import socket
import states
import udp_package
import client_debug
import thread_alive
from errors import NotAliveException

# Paquetes
REG_REQ = 'REG_REQ'
REG_INFO = 'REG_INFO'
REG_ACK = 'REG_ACK'
INFO_ACK = 'INFO_ACK'
REG_NACK = 'REG_NACK'
INFO_NACK = 'INFO_NACK'
REG_REJ = 'REG_REJ'
ALIVE = 'ALIVE'
ALIVE_REJ = 'ALIVE_REJ'

PDU_UDP_PACKAGE_SIZE = 84

MAX_REGISTRATION_ATTEMPTS = 3

CLIENT_IP = socket.gethostbyname(socket.gethostname())

# Etiquetas para calcular tiempos de envio/recepción de paquete de registro
T, U, N, O, P, Q, V, R = 1, 2, 7, 3, 3, 3, 2, 2


class Client(object):
    """ Aquetsa classe representa el client
    """

    def __init__(self, _configuration, _debug):
        self.state = states.States()
        self.udp_package = udp_package.UDPPackage()
        self.configuration = _configuration
        self.debug = client_debug.Debug(_debug)
        self.server_info = {}
        self.registration_attempts = 0

    def run(self):
        """ Arranca el client, passant per les següents fases:
            - Registre
            - Manteniment de la comunicació
            - Enviament de dades al servidor
            - Recepció de dades del servidor

        """
        try:
            self.debug.start_loop_service(configuration['Id'])
            if not self.registry():
                sys.exit(1)
        except KeyboardInterrupt:
            self.debug.control_C()
            self.close_threads()
            sys.exit()

    def registry(self):
        """ Inicia el procés d'enregistrament al servidor
        """

        self.state_not_registered()

    def state_not_registered(self):
        """ Estat: NOT_REGISTERED
            Inicia procés d'enregistrament, i envia el paquet REG_REQ
        """

        global pack, udp_sock

        self.registration_attempts += 1

        # Si el número d'enregistraments que es poden fer superen el màxim, el client finalitza
        if self.registration_attempts > MAX_REGISTRATION_ATTEMPTS:
            self.state.to_not_registered()
            self.debug.state_change(self.state.get_actual_state())
            self.debug.could_not_register(MAX_REGISTRATION_ATTEMPTS)
            return False

        # Passem al estat NOT_REGISTERED
        self.state.to_not_registered()
        self.debug.state_change(self.state.get_actual_state())
        self.debug.new_registration_process(self.state.get_actual_state(), self.registration_attempts)

        # Instanciem el socket en mode UDP
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Creem el paquet REG_REG, i l'enciem al servidor
        pack = self.udp_package.pack(REG_REQ, configuration['Id'])
        udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
        self.debug.send_udp_package(self.udp_package.get_last_package())

        # Passem a l'estat WAIT_ACK_REG
        return self.state_wait_ack_reg()

    def state_wait_ack_reg(self):
        """ Estat: WAIT_ACK_REG
            S'espera la resposta per part del servidor del paquet REG_REQ
        """

        global pack, udp_sock

        # El client passa a l'estat WAIT_ACK_REG
        self.state.to_wait_ack_reg()
        self.debug.state_change(self.state.get_actual_state())

        # Esperamos la respuesta del servidor
        answer = self.__wait_reg_req_response(T, U, N - 1, O, P - 1, Q)

        # Si no obtenim resposta, s'inicia una nova fase d'enregistrament, tornant a l'estat NOT_REGISTERED
        if answer is None:
            return self.__new_registration_process()

        # Desempaquetamos la entrada, y analizamos el paquete
        unpacked = self.udp_package.unpack(answer)
        self.debug.received_udp_package(self.udp_package.get_last_package())

        # Mirem si el paquet es tracta de REG_NACK, REG_ACK o REG_REJ
        if unpacked['type'] == REG_NACK:
            self.debug.discarded_package_with_reason(unpacked['data'])

            self.state.to_not_registered()
            self.debug.state_change(self.state.get_actual_state())

            # Creem el paquet REG_REG, i l'enciem al servidor
            pack = self.udp_package.pack(REG_REQ, configuration['Id'])
            udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

            return self.state_wait_ack_reg()

        elif unpacked['type'] == REG_ACK:
            # Enmagatzemem el id, random i les dades del servidor
            self.server_info['id'] = unpacked['id']
            self.server_info['random'] = unpacked['random']
            self.server_info['server-udp'] = unpacked['data']

            # Creem el paquet REG_INFO, i l'enviem
            pack = self.udp_package.pack(REG_INFO,
                                         configuration['Id'],
                                         self.server_info['random'],
                                         configuration['Server-UDP'] + ',' + configuration['Params'])

            udp_sock.sendto(pack, (self.configuration['Server'], int(self.server_info['server-udp'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

            # Passem a l'estat WAIT_ACK_INFO
            return self.state_wait_ack_info()

        elif unpacked['type'] == REG_REJ:
            # Rebutgem el paquet i s'inicia una nova fase d'enregistrament
            self.debug.package_rejected_with_reason(unpacked['data'])
            return self.__new_registration_process()

    def state_wait_ack_info(self):
        """ Estat: WAIT_ACK_INFO
            S'espera la resposta per part del servidor del paquet REG_INFO
        """

        global pack, udp_package

        # Passem a l'estat WAIT_ACK_INFO
        self.state.to_wait_ack_info()
        self.debug.state_change(self.state.get_actual_state())

        try:
            # Rebem el paquet i el desempaquetem
            answer = udp_sock.recv(PDU_UDP_PACKAGE_SIZE)
            unpacked = self.udp_package.unpack(answer)
            self.debug.received_udp_package(self.udp_package.get_last_package())
        except socket.timeout:
            # Si no obtenim resposta, s'inicia una nova fase d'enregistrament, tornant a l'estat NOT_REGISTERED
            self.debug.does_not_respond(REG_INFO)
            return self.__new_registration_process()

        # Comprovem la validesa del paquet
        if not self.package_validation(unpacked):
            return self.__new_registration_process()

        if unpacked['type'] == INFO_ACK:
            # Si el paquet es INFO_ACK, es passa a l'estat REGISTERED
            self.debug.accepted_device()
            return self.state_registered()

        elif unpacked['type'] == INFO_NACK:
            # Si el paquet es INFO_NACK, es passa a la fase d'enregistrament
            self.debug.discarded_package_with_additional_info(unpacked['data'])

            self.state.to_not_registered()
            self.debug.state_change(self.state.get_actual_state())

            # Creem el paquet REG_REG, i l'enciem al servidor
            pack = self.udp_package.pack(REG_REQ, configuration['Id'])
            udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

            return self.state_wait_ack_reg()

    def state_registered(self):
        """ Estat: REGISTERED
            Es dona per conclosa la fase d'enregistrament
            S'espera la resposta per part del servidor del paquet ALIVE, mantenint la connexió activa
        """
        global pack, udp_package

        # Es passa a l'estat REGISTERED
        self.state.to_registered()
        self.debug.state_change(self.state.get_actual_state())

        self.registration_attempts = 0

        for r in range(1, R):
            pack = self.udp_package.pack(ALIVE, configuration['Id'], self.server_info['random'])
            udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

            try:
                answer = udp_sock.recv(PDU_UDP_PACKAGE_SIZE)
                unpacked = self.udp_package.unpack(answer)
                self.debug.received_udp_package(self.udp_package.get_last_package())

            except socket.timeout:
                return self.__new_registration_process()

            finally:
                break

        if not self.package_validation(unpacked):
            return self.__new_registration_process()

        if unpacked['type'] == ALIVE_REJ:
            self.debug.rejected_alive()
            return self.__new_registration_process()

        elif unpacked['type'] == ALIVE:
            return self.state_send_alive()

    def state_send_alive(self):

        global t_alive

        self.debug.open_tcp_port(configuration['Local-TCP'])

        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # tcp_sock.connect((configuration['Server'], int(configuration['Local-TCP'])))

        self.state.to_send_alive()
        self.debug.state_change(self.state.get_actual_state())


        t_alive = thread_alive.AliveThread(udp_sock, 
                                           self.udp_package,
                                           self.debug,
                                           self.state, 
                                           self.configuration,
                                           self.server_info)
        self.debug.created_process_alive()
        t_alive.start()


        t_alive.join()

        udp_sock.close()
        self.debug.closed_udp_socket()

        tcp_sock.close()
        self.debug.closed_tcp_socket()

        return self.__new_registration_process()


    # FUNCIÓ PENDENT D'OPTIMITZACIÓ
    def __wait_reg_req_response(self, t, u, n, o, p, q):
        """ Per a no saturar la xarxa, aquesta funció anirà variant els temps en què és reenviant els paquets REG_REQ,
            en cas que el servidor no respongui
        """
        global udp_sock

        answer = None
        udp_sock.settimeout(t)

        # Enviem el paquet p vegades, sense variar el temps
        while p > 0:
            n -= 1
            try:
                answer = udp_sock.recv(84)
                if answer is not None:
                    return answer
            except socket.timeout:
                p -= 1
            udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

        # Cada vegada que enviem un paquet, s'augmenta el temps en 1, fins arribar a tq
        t += 1
        while t < T * q:
            udp_sock.settimeout(t)
            n -= 1
            try:
                answer = udp_sock.recv(PDU_UDP_PACKAGE_SIZE)
                if answer is not None:
                    return answer
            except socket.timeout:
                t += 1

            udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

        # Si el número de paquets enviats es n, finalitza
        while n > 0:
            udp_sock.settimeout(t)
            n -= 1
            try:
                answer = udp_sock.recv(PDU_UDP_PACKAGE_SIZE)
                if answer is not None:
                    return answer
            except socket.timeout:
                pass
            udp_sock.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
            self.debug.send_udp_package(self.udp_package.get_last_package())

        try:
            answer = udp_sock.recv(PDU_UDP_PACKAGE_SIZE)
            if answer is not None:
                return answer
        except socket.timeout:
            pass

        udp_sock.settimeout(T)
        return answer

    def package_validation(self, package):
        """ Comprova que els paquets arriben en l'estat i en el format correctes
        """

        if package['type'] == REG_ACK and not self.state.is_wait_ack_reg():
            return self.__new_registration_process()
        elif package['type'] == REG_NACK:
            return True
        elif package['type'] == REG_REJ:
            return True
        elif package['type'] == INFO_ACK or package['type'] == INFO_NACK:
            if not self.state.is_wait_ack_info():
                return False

            elif package['id'] != self.server_info['id']:
                self.debug.error_in_server_identification(CLIENT_IP, package['id'])
                return False

            elif package['random'] != self.server_info['random']:
                self.debug.random_error(package['random'], self.server_info['random'])
                return False

            else:
                return True
        elif package['type'] == ALIVE or package['type'] == ALIVE_REJ:
            if not self.state.is_send_alive() and not self.state.is_registered():
                return False

            elif package['id'] != self.server_info['id']:
                self.debug.error_in_server_identification(CLIENT_IP, package['id'])
                return False

            elif package['random'] != self.server_info['random']:
                self.debug.random_error(package['random'], self.server_info['random'])
                return False
            
            else:
                return True
        else:
            return False

    def __new_registration_process(self):
        """ Inicia un nou procés d'enregistrament
        """

        time.sleep(U)
        return self.state_not_registered()

    def close_threads(self):
        try:
            t_alive.kill()
        except NameError:
            pass


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
    parser.add_option('-c', '--configuration', action='store', type='string', default='client.cfg',
                      help='File of configurations')
    parser.add_option('-d', '--debug', action='store_true', default='false', help='Debuging?')
    (options, args) = parser.parse_args()

    configuration = read_configuration(options.configuration)

    client = Client(configuration, options.debug)

    client.run()
