
# Estados
NOT_REGISTERED = 'NOT_REGISTERED'
WAIT_ACK_REG = 'WAIT_ACK_REG'
WAIT_INFO = 'WAIT_INFO'
WAIT_ACK_INFO = 'WAIT_ACK_INFO'
REGISTERED = 'REGISTERED'
SEND_ALIVE = 'SEND_ALIVE'

class States(object):
    """Esta clase representa los estados en los que se puede encontrar un cliente

    """

    def __init__(self, state = NOT_REGISTERED):
        self.actual_state = state

    def get_actual_state(self):
        return self.actual_state

    def to_not_registered(self):
        self.actual_state = NOT_REGISTERED

    def to_wait_ack_reg(self):
        self.actual_state = WAIT_ACK_REG

    def to_wait_info(self):
        self.actual_state = WAIT_INFO

    def to_wait_ack_info(self): 
        self.actual_state = WAIT_ACK_INFO

    def to_registered(self):
        self.actual_state = REGISTERED

    def to_send_alive(self):
        self.actual_state = SEND_ALIVE


    def is_not_registered(self):
        self.actual_state == NOT_REGISTERED

    def is_wait_ack_reg(self):
        self.actual_state == WAIT_ACK_REG

    def is_wait_info(self):
        self.actual_state == WAIT_INFO

    def is_wait_ack_info(self): 
        self.actual_state == WAIT_ACK_INFO

    def is_registered(self):
        self.actual_state == REGISTERED

    def is_send_alive(self):
        self.actual_state == SEND_ALIVE

    def show(self):
        print(self.actual_state)