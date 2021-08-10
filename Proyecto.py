#Andrea Estefania Elias Cobar
# 17048
# Redes
# Ing Jorge Yass

# Chat Bot extraido de la guia de slixmpp


#!/usr/bin/env python3

# Slixmpp: The Slick XMPP Library
# Copyright (C) 2010  Nathanael C. Fritz
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.

import logging
from getpass import getpass
from argparse import ArgumentParser
import slixmpp


class Register(slixmpp.ClientXMPP):
    ### Inicializacion del objeto ClientXMPP que va a crear al usuario durante su registro
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)


        

        ### A continuacion se realiza la llamada de metodos inicializadores
        ### que manejaran los eventos de iniciar sesion y registrar
        self.user = jid
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

    ### Metodo que inicia la sesion del usuario a registrar
    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.disconnect()

    ### Metodo que permite el registro de un usuario a través de una stanza
    ### generada con IQ
    def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

    ### Se hace un envio de la stanza a la espera de que esta pueda crear
    ### el usuario que se pretende registrar
        try:
            resp.send()
            print("Cuenta creada para", self.boundjid,"\n")
        except IqError as e:
            print("No fue posible registrar la cuenta: ", e,"\n")
            self.disconnect()
        except IqTimeout:
            print("El servidor no responde\n")
            self.disconnect()




class SendMsgBot(slixmpp.ClientXMPP):

    """
    A basic Slixmpp bot that will log in, send a message,
    and then log out.
    """

    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        # The message we wish to send, and the JID that
        # will receive it.
        self.user = jid
        self.recipient = recipient
        self.msg = message

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

        if(self.msg != ""):
            self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')
        

        self.disconnect()


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser(description=SendMsgBot.__doc__)

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")
    parser.add_argument("-t", "--to", dest="to",
                        help="JID to send the message to")
    parser.add_argument("-m", "--message", dest="message",
                        help="message to send")
    parser.add_argument("-r", "--register", dest="register",
                        help="Is new user")

    


    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    client = True
    menu = True
    while menu:
        if (client == True):
            opcion = int(input("Que desea realizar\n1. Registrar cuenta\n2. Iniciar sesion\n"))
            
            
            if (opcion == 1):
                print("Porfavor ingrese los siguientes datos :)")
                args.jid = input("Usuario: ")
                #Se uutiliza la libreria getpass en orden de ocultarla
                args.password =  getpass(prompt='Contraseña: ')
                xmpp = SendMsgBot(args.jid, args.password,"","")
                xmpp.connect()
                xmpp.process(forever=False)
                client = False
                #break

            elif (opcion == 2):

                print("Por favor ingrese lo siguiente")

                if args.jid is None:
                    
                    args.jid = input("Usuario: ")
                if args.password is None:
                    args.password = getpass("Contraseña: ")
                xmpp = Register(args.jid, args.password)
                xmpp.register_plugin('xep_0030')
                xmpp.register_plugin('xep_0004') 
                xmpp.register_plugin('xep_0066') 
                xmpp.register_plugin('xep_0077') 
                xmpp.connect()
                xmpp.process(forever=False)
        else:
            opcion = int(input("Que desea realizar: \n1. Cerrar sesion\n2. Eliminar cuenta\n3. Mostrar mis contactos y estado\n4. Agregar contacto\n5. Mostrar detalles de un contacto\n6. Enviar mensaje\n7. Unir a grupo\n8. Enviar mensaje a grupo\n9. Mensaje de presencia\n10. Enviar archivo\n11. Usuarios del server\n12. Salir\n"))
            if(opcion==1):
                if args.to is None:
                    args.to = input("Ingrese el usuario de su destinatario: ")
                if args.message is None:
                    args.message = input("Ingrese su mensaje: ")
                xmpp = SendMsgBot(args.jid,args.password,args.to,args.message)
                xmpp.connect()
                xmpp.process(forever=False)


            if(opcion==6):
                if args.to is None:
                    args.to = input("Ingrese el usuario de su destinatario: ")
                if args.message is None:
                    args.message = input("Ingrese su mensaje: ")
                xmpp = SendMsgBot(args.jid,args.password,args.to,args.message)
                xmpp.connect()
                xmpp.process(forever=False)

 