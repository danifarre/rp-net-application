#! /usr/bin/python

# Clase que representa els estats possibles d'un client
class States:
    actual_state = ""

    def __init__(self, state = "NOT_REGISTERED"):
        self.actual_state = state

    def get_actual_state(self):
        return self.actual_state

    def to_NOT_REGISTERED(self):
        self.actual_state = "NOT_REGISTERED"

    def to_WAIT_ACK_REG(self):
        self.actual_state = "WAIT_ACK_REG"

    def to_WAIT_INFO(self):
        self.actual_state = "WAIT_INFO"

    def to_WAIT_ACK_INFO(self): 
        self.actual_state = "WAIT_ACK_INFO"

    def to_REGISTERED(self):
        self.actual_state = "REGISTERED"

    def to_SEND_ALIVE(self):
        self.actual_state = "SEND_ALIVE"

    def show(self):
        print self.actual_state