import time

class Debug(object):
	
    def __init__(self):
        pass

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

    def info_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'INFO  =>  '

    def discarded_package_with_reason(self, reason):
        print(self.info_start() + 'Descartat paquet de subscripció enviat, motiu: ' + reason)

    def package_rejected_with_reason(self, reason):
        print(self.info_start() + 'Rebutjat paquet de subscripció enviat, motiu: ' + reason)

    def discarded_package_with_additional_info(self, reason):
        print(self.info_start() + 'Descartat paquet de informació adicional de subscripció, motiu: ' + reason)

    #################################################################################

    # Mensajes de DEBUG
    #################################################################################

    def debug_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'DEBUG =>  '

    def start_loop_service(self, id):
        print(self.debug_start() + 'Inici bucle de servei del equip: ' + id)

    def send_udp_package(self, package):
        size, pack, id, rndm, data = package
        print(self.debug_start() + 'Enviat: ' + 
                                    'bytes=' + str(size) + ', ' + 
                                    'paquet=' + pack + ', ' +
                                    'id=' + id + ', ' + 
                                    'rndm=' + rndm + ', ' + 
                                    'dades=' + data
                                    )

    def received_udp_package(self, package):
        size, pack, id, rndm, data = package
        print(self.debug_start() + 'Rebut: ' + 
                                    'bytes=' + str(size) + ', ' + 
                                    'paquet=' + pack + ', ' +
                                    'id=' + id + ', ' + 
                                    'rndm=' + rndm + ', ' + 
                                    'dades=' + data
                                    )

    def accepted_device(self):
        print(self.debug_start() + 'Acceptada la subscripció del dispositiu en el servidor')

    #################################################################################

    # Mensajes de MESSAGE
    #################################################################################
    
    def msg_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'MSG.  =>  '

    def new_registration_process(self, state, attempt):
        print(self.msg_start() + "Dispositiu passa a l'estat: " + state + ', proceso de suscripción: ' + str(attempt))
    
    def state_change(self, state):
        print(self.msg_start() +  "Dispositiu passa a l'estat: " + state)

    def could_not_register(self, attempts):
        print(self.msg_start() + 'Superat el número de processos de suscripció (' + str(attempts) +')')

    #################################################################################