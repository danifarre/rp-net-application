import threading
import socket
import sys
import os
import time
import udp_package
import client_debug
import states

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


V = 2
S = 2

class AliveThread(threading.Thread): 
    def __init__(self, _socket, _udp_package, _debug, _state, _configuration, _server_info): 
        threading.Thread.__init__(self)
        self.pid = None
        self.socket = _socket
        self.udp_package = _udp_package
        self.debug = _debug
        self.state = _state
        self.configuration = _configuration
        self.server_info = _server_info
        self.killed = False
        self.alive_rej = False

    def get_pid(self):
        return self.pid

    def kill(self):
        self.debug.ended_process(os.getpid())
        self.killed = True

    def is_killed(self):
        return self.killed

    def recieved_alive_rej(self):
        return self.alive_rej
        
    def run(self): 
        s = S
        while not self.is_killed():
            time.sleep(V)

            if not self.is_killed():
                pack = self.udp_package.pack(ALIVE, self.configuration['Id'], self.server_info['random'])
                self.socket.sendto(pack, (self.configuration['Server'], int(self.configuration['Server-UDP'])))
                self.debug.send_udp_package(self.udp_package.get_last_package())

                try:
                    answer =self.socket.recv(PDU_UDP_PACKAGE_SIZE)
                    unpacked = self.udp_package.unpack(answer)
                    self.debug.received_udp_package(self.udp_package.get_last_package())

                except socket.timeout:
                    s -= 1
                    if s == 0:
                        self.kill()
                        break 
                    continue

                if not self.package_validation(unpacked):
                    self.kill()
                    break

                if unpacked['type'] == ALIVE_REJ:
                    self.debug.rejected_alive()
                    self.kill()
                    self.alive_rej = True
                    break


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
