#! /usr/bin/python

import sys
import states

class Client:
    def __init__(self, configuration, debug):
        self.state = states.States()
        self.configuration = configuration
        self.debug = debug

    def run(self):
        pass

def read_configuration(file_name):
    configuration = []
    
    with open(file_name) as f:
        for line in f:
            configuration.append(line[line.index("=") + 1: -1])

    return configuration


if __name__ == "__main__":
    configuration = []
    debug = False

    if "-c" in sys.argv:
        configuration = read_configuration(sys.argv[sys.argv.index("-c") + 1])
    else:
        configuration = read_configuration("client.cfg")

    if "-d" in sys.argv:
        debug = True

    client = Client(configuration, debug)

    client.run()