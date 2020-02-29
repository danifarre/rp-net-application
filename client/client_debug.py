import time

class Debug(object):
	
    def __init__(self):
        self.suscription_process = 0

    # Mensajes de ERROR
    #################################################################################

    def debug_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'ERR.  =>  '

    #################################################################################

    # Mensajes de WARNING
    #################################################################################

    def debug_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'WARN  =>  '

    #################################################################################

    # Mensajes de ALERT
    #################################################################################

    def debug_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'ALERT =>  '

    #################################################################################

    # Mensajes de INFO
    #################################################################################

    def debug_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'INFO  =>  '

    #################################################################################

    # Mensajes de DEBUG
    #################################################################################

    def debug_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'DEBUG =>  '

    def start_loop_service(self, id):
        print(self.debug_start() + 'Inicio bucle de servicio del equipo: ' + id)

    def send_udp_package(self, package):
        size, pack, id, rndm, data = package
        print(self.debug_start() + 'Enviado: ' + 
                                    'bytes=' + str(size) + ', ' + 
                                    'paquete=' + pack + ', ' +
                                    'id=' + id + ', ' + 
                                    'rndm=' + rndm + ', ' + 
                                    'datos=' + data
                                    )

    def received_udp_package(self, package):
        size, pack, id, rndm, data = package
        print(self.debug_start() + 'Recibido: ' + 
                                    'bytes=' + str(size) + ', ' + 
                                    'paquete=' + pack + ', ' +
                                    'id=' + id + ', ' + 
                                    'rndm=' + rndm + ', ' + 
                                    'datos=' + data
                                    )

    def accepted_device(self):
        print(self.debug_start() + 'Aceptada la suscripción del dispositivo en el servidor')

    #################################################################################

    # Mensajes de MESSAGE
    #################################################################################
    def msg_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'MSG.  =>  '

    def new_registration_process(self, state):
        self.suscription_process += 1
        print(self.msg_start() + 'Dispositivo pasa a estado: ' + state + ', proceso de suscripción: ' + str(self.suscription_process))
    
    def state_change(self, state):
        print(self.msg_start() + 'Dispositivo pasa a estado: ' + state)

    #################################################################################