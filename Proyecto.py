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
from getpass import getpass #libreria para ocultar contraseña
from argparse import ArgumentParser
import slixmpp

### Clase utilizada para hacer un registro de usuario en el servidor
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
        iq = self.Iq()
        iq['type'] = 'set'
        iq['register']['username'] = self.boundjid.user
        iq['register']['password'] = self.password

 ### Se hace un envio de la stanza a la espera de que esta pueda crear
### el usuario que se pretende registrar
        try:
            iq.send()
            print("Cuenta creada para ", self.boundjid,"\n")
        except IqError as e:
            print("Ups. No fue posible registrar la cuenta:", e,"\n")
            self.disconnect()
        except IqTimeout:
            print("El servidor no responde\n")
            self.disconnect()
        except Exception as e:
            print(e)
            self.disconnect()  



class Cliente(slixmpp.ClientXMPP):

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

        self.mis_contactos = []

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)
    
    def cerrar_sesion(self):
        for jid in self.mis_contactos:
            ### Envio de notificacion para avisar el cierre de sesion por medio de un mensaje
            self.notificacion_chat(jid, 'Adiós amigos mios', 'inactive')
        ### Aqui cerramos la sesion del usuario
        self.disconnect(wait=False)
        print("Sesión cerrada")
       
        

    def start(self, event):
        """
        Process the session_start event.
        Typical actions for the sesself.add_event_handler("register", self.register)ion_start event are
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
        # await self.get_roster()





        

        # self.disconnect()


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser(description=Cliente.__doc__)

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

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    notOnline = True
    cliente = None
    menu = True
    while menu:
        if (notOnline == True and cliente==None):
            
            opcion= input("1. Iniciar sesion \n2. Registrar nuevo usuario\n")
            if (opcion== "1"):
                args.jid = input("Usuario: ")
                args.password =  getpass(prompt='Contraseña: ')
                xmpp =Cliente(args.jid, args.password,"","")
                xmpp.connect()
                xmpp.process(forever=False)
                notOnline = False
            elif (opcion== "2"):
                if args.jid is None:
                    args.jid = input("Ingrese su nombre de usuario: ")
                if args.password is None:
                    args.password = getpass("Por favor ingrese su contraseña: ")
                xmpp = Register(args.jid, args.password)
                xmpp.register_plugin('xep_0066') 
                xmpp.register_plugin('xep_0077') 
                xmpp.register_plugin('xep_0030') 
                xmpp.register_plugin('xep_0004') 
                cliente = Cliente(args.jid, args.password,"","")
                
                xmpp.connect()
                xmpp.process(forever=False)
        else:
            opcion= input("\n1. Cerrar sesion\n2. Eliminar cuenta\n3. Mostrar mis contactos y estado\n4. Agregar contacto\n5. Mostrar detalles de un contacto\n6. Enviar mensaje\n7. Unir a grupo\n8. Enviar mensaje a grupo\n9. Mensaje de presencia\n10. Enviar archivo\n11. Usuarios del server\n12. Salir\n")
            
            if(opcion =="1"):
                cliente.cerrar_sesion()
                cliente = None
            
            if(opcion=="6"):
                if args.to is None:
                    args.to = input("Ingrese el usuario del destinatario a quien desea enviar un mensaje ")
                if args.message is None:
                    args.message = input("Escriba su mensaje: ")
                xmpp =Cliente(args.jid,args.password,args.to,args.message)
                xmpp.connect()
                xmpp.process(forever=False)

 