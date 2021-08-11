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
from os import name
import slixmpp
from slixmpp.exceptions import XMPPError
from slixmpp.xmlstream import ET, tostring
from slixmpp import Iq
from slixmpp.exceptions import IqError, IqTimeout
import base64, time
import agregarContacto
from agregarContacto import *


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

class eliminar_account(slixmpp.ClientXMPP):

    def __init__(self, usuario, contraseña):

        slixmpp.ClientXMPP.__init__(self, usuario, contraseña)

        self.user = usuario
        self.add_event_handler("session_start", self.start)


    def start(self, event):
        self.send_presence()
        self.get_roster()
        delete =  self.Iq()
        delete['type'] = 'set'
        delete['from'] = self.user
        delete['id'] = 'del'


        fragmentoStanza =  ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")

        ### Se agrega la stanza custom para remove register
        delete.append(fragmentoStanza)

        ### Se hace el envio de la stanza para hacer el unregister de la cuenta
        try:
            delete.send()
            print("Cuenta eliminada")
        except IqError as e:
            print("No es posible eliminar la cuenta", e)
        except IqTimeout:
            print("El servidor no responde")


    




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
    
    def eliminar_cuenta(self, jid):
        ### Se crea una stanza de tipo IQ para mandar un request de remove register
        delete =  self.Iq()
        delete['type'] = 'set'
        delete['from'] = jid
        delete['id'] = 'del'


        fragmentoStanza =  ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")

        ### Se agrega la stanza custom para remove register
        delete.append(fragmentoStanza)

        ### Se hace el envio de la stanza para hacer el unregister de la cuenta
        try:
            delete.send()
            print("Cuenta eliminada")
        except IqError as e:
            print("No es posible eliminar la cuenta", e)
        except IqTimeout:
            print("El servidor no responde")

 

    



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
    #cliente = None
    menu = True
    while menu:
        if (notOnline == True  ):#cliente==None):
            
            opcion= input("1. Iniciar sesion \n2. Registrar nuevo usuario\n")
            if (opcion== "1"):
                args.jid = input("Usuario: ")
                args.password =  getpass(prompt='Contraseña: ')
                xmpp =Cliente(args.jid, args.password,"","")
                #cliente = Cliente(args.jid, args.password, "","")
                xmpp.connect()
                xmpp.process(forever=False)
                notOnline = False
                #cliente = Cliente(args.jid, args.password,"","")
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
                #jid = Cliente(args.jid, args.password,"","")
                xmpp.connect()
                xmpp.process(forever=False)
        else:
           
            opcion= input("\n1. Cerrar sesion\n2. Eliminar cuenta\n3. Mostrar mis contactos y estado\n4. Agregar contacto\n5. Mostrar detalles de un contacto\n6. Enviar mensaje\n7. Unir a grupo\n8. Enviar mensaje a grupo\n9. Mensaje de presencia\n10. Enviar archivo\n11. Usuarios del server\n12. Salir\n")
            
            if(opcion =="1"):
                cliente.cerrar_sesion()
                cliente = None
            
            elif opcion == "2" :#and cliente != None:
                args.jid = input("Ingrese el usuario a eliminar: ")
                xmpp = eliminar_account(args.jid,args.password)
                xmpp.connect()
                xmpp.process(forever=False)
                #ciente = None
            
            elif opcion == "3":
                print("Buscando contactos")
                contactos = xmpp.contactos_estado()
                print("Mis contactos son:\n|Usuario|---|Nombre|---|Subscripción|--|Estado|\n")
                for contacto in contactos:
                    print(contacto)

            elif opcion == "4":
                usuario = input("Ingrese la cuenta del usuario a agregar: ")
                #nombre = input("Ingresa el nombre del usuario: ")
                xmpp = agregar_contacto(args.jid, args.password, usuario)
                xmpp.connect()
                xmpp.process(forever = False)

            

                            
            
            elif(opcion=="6"):
                if args.to is None:
                    args.to = input("Ingrese el usuario del destinatario a quien desea enviar un mensaje ")
                if args.message is None:
                    args.message = input("Escriba su mensaje: ")
                xmpp =Cliente(args.jid,args.password,args.to,args.message)
                xmpp.connect()
                xmpp.process(forever=False)


            elif(opcion == "10"):
                usuario = input("Ingrese la cuenta del usuario a enviar el archivo: ")
                archivo = input("Ingrese el path del documento: ")
                xmpp.enviar_archivo(usuario, archivo)

 