import time

class Debug(object):
	
    def __init__(self, _debug):
        self.debug = _debug

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

    def alert_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'ALERT =>  '

    def error_in_server_identification(self, client_ip, id):
        if self.debug == True:
            print(self.alert_start() + "Error en les dades d'identificació del servidor (rebut ip: " + client_ip + ", id: " + id + ")")


    #################################################################################

    # Mensajes de INFO
    #################################################################################

    def info_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'INFO  =>  '

    def discarded_package_with_reason(self, reason):
        if self.debug == True:
            print(self.info_start() + 'Descartat paquet de subscripció enviat, motiu: ' + reason)

    def package_rejected_with_reason(self, reason):
        if self.debug == True:
            print(self.info_start() + 'Rebutjat paquet de subscripció enviat, motiu: ' + reason)

    def discarded_package_with_additional_info(self, reason):
        if self.debug == True:
            print(self.info_start() + 'Descartat paquet de informació adicional de subscripció, motiu: ' + reason)

    #################################################################################

    # Mensajes de DEBUG
    #################################################################################

    def debug_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'DEBUG =>  '

    def start_loop_service(self, id):
        if self.debug == True:
            print(self.debug_start() + 'Inici bucle de servei del equip: ' + id)

    def send_udp_package(self, package):
        if self.debug == True:
            size, pack, id, rndm, data = package
            print(self.debug_start() + 'Enviat: ' + 
                                        'bytes=' + str(size) + ', ' + 
                                        'paquet=' + pack + ', ' +
                                        'id=' + id + ', ' + 
                                        'rndm=' + rndm + ', ' + 
                                        'dades=' + data
                                        )

    def received_udp_package(self, package):
        if self.debug == True:
            size, pack, id, rndm, data = package
            print(self.debug_start() + 'Rebut: ' + 
                                        'bytes=' + str(size) + ', ' + 
                                        'paquet=' + pack + ', ' +
                                        'id=' + id + ', ' + 
                                        'rndm=' + rndm + ', ' + 
                                        'dades=' + data
                                        )

    def accepted_device(self):
        if self.debug == True:
            print(self.debug_start() + 'Acceptada la subscripció del dispositiu en el servidor')

    def random_error(self, actual, expected):
        if self.debug == True:
            print(self.debug_start() + 'Error en el valor del camp rndm (rebut: ' + actual + ', ' + 'esperat: ' + expected+ ')')

    def does_not_respond(self, name):
        if self.debug == True:
            print(self.debug_start() +  'Temporització per manca de resposta al paquet enviat: ' + name)
        
    #################################################################################

    # Mensajes de MESSAGE
    #################################################################################
    
    def msg_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'MSG.  =>  '

    def new_registration_process(self, state, attempt):
        if self.debug == True:
            print(self.msg_start() + "Dispositiu passa a l'estat: " + state + ', proceso de suscripción: ' + str(attempt))
    
    def state_change(self, state):
        print(self.msg_start() +  "Dispositiu passa a l'estat: " + state)

    def could_not_register(self, attempts):
        if self.debug == True:
            print(self.msg_start() + 'Superat el número de processos de suscripció (' + str(attempts) +')')

    #################################################################################