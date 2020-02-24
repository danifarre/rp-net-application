#! /usr/bin/python

import sys, optparse
import socket
import states

class Client:
    def __init__(self, configuration, debug):
        self.state = states.States()
        self.configuration = configuration
        self.debug = debug

    def run(self):
        self.registry()

    def registry(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto('(0x00) (' + configuration['id'] + ') ("00000000")' + ' ("")', (self.configuration['server'], int(self.configuration['server-udp'])))

def read_configuration(file_name):
    configuration = {}

    with open(file_name) as f:
        for line in f:
            configuration[line[: line.index('=')]] = line[line.index('=') + 1: -1]

    return configuration


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-c', '--configuration', action='store', type='string', default='client.cfg', help='File of configurations')
    parser.add_option('-d', '--debug', action='store_true', default='false', help='Debuging?')
    (options, args) = parser.parse_args()

    configuration = read_configuration(options.configuration)

    client = Client(configuration, options.debug)

    client.run()