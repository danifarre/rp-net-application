import time

class Debug(object):
	
    def __init__(self, _debug):
        self.debug = _debug

    def params(self, id, state, params):
        print('********************* DADES DISPOSITIU ***********************')
        print(' Identificador: ' + id)
        print(' Estat: ' + state)
        print()
        print('   ', end = '')
        print('Param         Valor')
        print('   ', end = '')
        print('-------     ---------------')
        for p, n in params.items():
            print('   ', end = '')
            print(p, end = '     ')
            print(n)
        print()
        print('**************************************************************')


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

    def send_tcp_package(self, package):
        if self.debug == True:
            size, pack, id, rndm, element, valor, info = package
            print(self.debug_start() + 'Enviat: ' + 
                                        'bytes=' + str(size) + ', ' + 
                                        'paquet=' + pack + ', ' +
                                        'id=' + id + ', ' + 
                                        'rndm=' + rndm + ', ' + 
                                        'element=' + element + ', ' +
                                        'valor=' + valor + ', ' +
                                        'info=' + info
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

    def received_tcp_package(self, package):
        if self.debug == True:
            size, pack, id, rndm, element, valor, info = package
            print(self.debug_start() + 'Rebut: ' + 
                                        'bytes=' + str(size) + ', ' + 
                                        'paquet=' + pack + ', ' +
                                        'id=' + id + ', ' + 
                                        'rndm=' + rndm + ', ' + 
                                        'element=' + element + ', ' +
                                        'valor=' + valor + ', ' +
                                        'info=' + info
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
    
    def ended_process(self, pid):
        if self.debug == True:
            print(self.debug_start() + 'Finalitzat procés ' + str(pid))

    def created_process_alive(self):
        if self.debug == True:
            print(self.debug_start() + 'Creat procés per enviament periòdic de ALIVE')

    def rejected_alive(self):
        if self.debug == True:
            print(self.debug_start() + 'Rebut paquet de rebuig ALIVE')

    def closed_udp_socket(self):
        if self.debug == True:
            print(self.debug_start() + 'Tancat socket UDP per la comunicació amb el servidor')

    def closed_tcp_socket(self):
        if self.debug == True:
            print(self.debug_start() + 'Tancat socket TCP per la comunicació amb el servidor')

    def timer_alive(self):
        if self.debug == True:
            print(self.debug_start() + 'Establert temporitzador per enviament de ALIVE')


    def error_in_client_identification(self, id):
        if self.debug == True:
            print(self.debug_start() + "Error en les dades d'identificació del dispositiu (rebut id: " + id + ")")

    def error_in_client_identification_2(self, id):
            if self.debug == True:
                print(self.debug_start() + 'Rebut paquet amb id dispositiu incorrecte: ' + id + ' (error identificació)')

    def accepted_data(self, element, valor, info):
        if self.debug == True:
            print(self.debug_start() + "Acceptat l'enviament de dades (element: " + element + ", valor: " + valor + "). Info: " + info)


    def recieved_element_identifer_error(self, element, valor):
        if self.debug == True:
            print(self.debug_start() + "Error en les dades d'identificació de l'element del dispositiu (rebut element: " + element + ", valor: " + valor + ")")
    
    def resend_data(self):
        if self.debug == True:
             print(self.debug_start() + "Caldria reenviar les dades al servidor")

    def ignored_send_data(self):
        if self.debug == True:
            print(self.debug_start() + "Rebut paquet de confirmació ALIVE sense confirmacions pendents. Paquet ignorat")

    def package_error_in_server_identification(self, id, random, server_ip):
        if self.debug == True:
            print(self.debug_start() + "Rebut paquet incorrecte. Servidor: id=" + id + ", rndm=" + random + ", ip=" + server_ip + " (error identificació)")
    
    def package_error_in_client_identification(self, id):
        if self.debug == True:
            print(self.debug_start() + "Rebut paquet amb id dispositiu incorrecte: " + id + " (error identificació)")
    
    def error_output_element(self, element):
        if self.debug == True:
            print(self.debug_start() + "Error paquet rebut. Element: " + element + " és sensor i no permet establir el seu valor")

    #################################################################################

    # Mensajes de MESSAGE
    #################################################################################
    
    def msg_start(self):
        return time.strftime("%H:%M:%S") + ': ' + 'MSG.  =>  '

    def control_C(self):
        print(self.msg_start() + 'Finalització per ^C')

    def new_registration_process(self, state, attempt):
        if self.debug == True:
            print(self.msg_start() + "Dispositiu passa a l'estat: " + state + ', proceso de suscripción: ' + str(attempt))
    
    def state_change(self, state):
        print(self.msg_start() +  "Dispositiu passa a l'estat: " + state)

    def could_not_register(self, attempts):
        if self.debug == True:
            print(self.msg_start() + 'Superat el número de processos de suscripció (' + str(attempts) +')')

    def open_tcp_port(self, port):
        if self.debug == True:
            print(self.msg_start() + 'Obert port TCP ' + port + ' per la comunicació amb el servidor')

    def wrong_command(self, command):
        if self.debug == True:
            print(self.msg_start() + 'Commanda incorrecta (' +  command + ')')

    def syntax_error(self, command):
        if self.debug == True:
            print(self.msg_start() + 'Error de sintàxi. (' +  command + ')')

    def element_does_not_exist(self, elem):
        if self.debug == True:
            print(self.msg_start() + 'Element: [' + elem + '] no pertany al dispositiu')

    def init_tcp_comunication(self, port):
        if self.debug == True:
            print(self.msg_start() + 'Iniciada comunicació TCP amb el servidor (port: ' + port + ')')

    def finish_tcp_comunication(self, port):
        if self.debug == True:
            print(self.msg_start() + 'Finalitzada comunicació TCP amb el servidor (port: ' + port + ')')


    #################################################################################