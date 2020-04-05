import sys
import os
import select
import threading
import socket
import states
import tcp_package
import client_debug
from datetime import datetime

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

SEND_DATA = 'SEND_DATA'
SET_DATA = 'SET_DATA'
GET_DATA = 'GET_DATA'
DATA_ACK = 'DATA_ACK'
DATA_NACK = 'DATA_NACK'
DATA_REJ = 'DATA_REJ'

STAT = 'stat'
SET = 'set'
SEND ='send'
QUIT = 'quit'

PDU_TCP_PACKAGE_SIZE = 127

M = 3



class InputThread(threading.Thread): 
    def __init__(self, _debug, _configuration, _server_info, _params, _state): 
        threading.Thread.__init__(self)
        self.killed = False
        self.command = []
        self.debug = _debug
        self.configuration = _configuration
        self.server_info = _server_info
        self.params = _params
        self.state = _state
        self.tcp_package = tcp_package.TCPPackage()
        self.quit = False

    def kill(self):
        tcp_sock.close()
        self.debug.ended_process(os.getpid())
        self.killed = True

    def is_killed(self):
        return self.killed


    def is_quit(self):
        return self.quit
        
    def run(self):
        global tcp_sock


        while not self.is_killed():
            command = self.get_command()

            tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_sock.settimeout(M)
            
            if command is not None:
                if command[0] == STAT:
                    self.debug.params(self.configuration['Id'], self.state.get_actual_state(), self.params)
                elif command[0] == SET:
                    self.params[command[1]] = command[2]
                elif command[0] == SEND:

                    if command[1] in self.params:
                        self.debug.init_tcp_comunication(self.server_info['server-tcp'])

                        pack = self.tcp_package.pack(SEND_DATA,
                                                     self.configuration['Id'], 
                                                     self.server_info['random'],
                                                     command[1],
                                                     self.params[command[1]],
                                                     datetime.today().strftime('%Y-%m-%d;%H:%M:%S'))


                        tcp_sock.connect((self.configuration['Server'], int(self.server_info['server-tcp'])))


                        tcp_sock.send(pack)
                        self.debug.send_tcp_package(self.tcp_package.get_last_package())

                        answer = None
                        try:
                            answer = tcp_sock.recv(PDU_TCP_PACKAGE_SIZE)
                        except socket.timeout:
                            self.debug.ignored_send_data()
                            self.debug.finish_tcp_comunication(self.server_info['server-tcp'])
                            continue

                        unpacked = self.tcp_package.unpack(answer)
                        self.debug.received_tcp_package(self.tcp_package.get_last_package())

                        if not self.package_validation(unpacked):
                            self.debug.finish_tcp_comunication(self.server_info['server-tcp'])
                            self.killed = True
                            break

                        if unpacked['type'] == DATA_ACK:
                            if command[1] != unpacked['element']:
                                self.debug.recieved_element_identifer_error(unpacked['element'], unpacked['valor'])
                                self.debug.resend_data()
                            else:
                                self.debug.accepted_data(unpacked['element'], unpacked['valor'], unpacked['info'])

                        elif unpacked['type'] == DATA_NACK:
                            self.debug.resend_data()

                        elif unpacked['type'] == DATA_REJ:
                            self.killed = True

                        self.debug.finish_tcp_comunication(self.server_info['server-tcp'])
                    else: 
                        self.debug.element_does_not_exist(command[1])

                elif command[0] == QUIT:
                    self.quit = True
                    self.killed = True
                    break

    def get_command(self):
        i, o, e = select.select( [sys.stdin], [], [], 0.5)

        if (i):
            command = input().split()
            if not self.valid(command):
                return None
            return command

    def valid(self, command):
        if len(command) > 0:
            if command[0] == STAT:
                if len(command) != 1:
                    self.debug.syntax_error(command[0])
                    return False
                return True

            elif command[0] == SET:
                if len(command) != 3:
                    self.debug.syntax_error(command[0])
                    return False
                return True

            elif command[0] == SEND:
                if len(command) != 2:
                    self.debug.syntax_error(command[0])
                    return False
                return True

            elif command[0] == QUIT:
                if len(command) != 1:
                    self.debug.syntax_error(command[0])
                return True

            else:
                self.debug.wrong_command(command[0])
                return False

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
            elif package['type'] == DATA_ACK or package['type'] == DATA_NACK or package['type'] == DATA_REJ:
                if not self.state.is_send_alive():
                    return False

                if package['info'] != self.configuration['Id']:
                    self.debug.error_in_client_identification(package['info'])
                    return False

                elif package['random'] != self.server_info['random']:
                    self.debug.random_error(package['random'], self.server_info['random'])
                    return False
                else:
                    return True
            else:
                return False
