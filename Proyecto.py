#Andrea Estefania Elias Cobar
# 17048
# Redes
# Ing Jorge Yass

# Codigo guiado de la guia de slixmpp para Python
# Se esta utilizando la version de python 3.7

#Librerias a utilizar
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


        
        

#clase para eliminar una cuenta
  

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

   

    def __init__(self, jid, password, recipient, message, xd):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        
        self.user = jid
        self.recipient = recipient
        self.msg = message
        self.mensajePresencia = xd
        self.mis_contactos = []



        # Se inicia sesion
        self.add_event_handler("session_start", self.start)


    
    
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

    
    def cerrar_sesion(self):
        
        ### Aqui cerramos la sesion del usuario
        self.disconnect(wait=False)
        print("Sesión cerrada")

 

    



    def start(self, event):
        
        #self.send_presence()
        self.get_roster()
        if(self.msg != ""):
            self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')
        if self.mensajePresencia != "":
            self.send_presence(pshow = "chat", pstatus = mensajePresencia)
        else:
            self.send_presence(pshow = "chat", pstatus = "Hola amixes")
        self.get_roster()
        self.disconnect()

        # if(self.msg != ""):
        #     self.send_message(mto=self.recipient,
        #                   mbody=self.msg,
        #                   mtype='chat')



       
        # await self.get_roster()





        

        # self.disconnect()


if __name__ == '__main__':
   
    parser = ArgumentParser(description=Cliente.__doc__)

   
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    # JID y contraseña
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

### <----------------------------------------------------------------------------------------------------------->
### MAIN - PROYECTO 2 PROTOCOLO XMPP
### Aqui se realiza el menu para poder utilizar el programa y sus funcionalidades del chat con protocolo XMPP
### Creamos una variable cliente y sala, ambas vacias, para luego poder manejar el resto de opciones

    EnLinea = True
    cliente = None
    menu = True
    while menu:
        if EnLinea == True and cliente == None :#cliente==None):
            
            opcion= input("1. Iniciar sesion \n2. Registrar nuevo usuario\n")


            if opcion== "1":
                args.jid = input("Usuario: ")
                args.password =  getpass(prompt='Contraseña: ')
                xmpp =Cliente(args.jid, args.password,"","","")
                #cliente = Cliente(args.jid, args.password, "","")
                xmpp.connect()
                xmpp.process(forever=False)
                EnLinea = False
                cliente = Cliente(args.jid, args.password,"","","")


            elif opcion== "2":
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
           
            opcion= input("\n1. Cerrar sesion\n2. Eliminar cuenta\n3. Mostrar mis contactos y estado\n4. Agregar contacto\n5. Mostrar detalles de un contacto\n6. Enviar mensaje\n7. Unir a grupo\n8. Enviar mensaje a grupo\n9. Mensaje de presencia\n10. Enviar archivo\n11. Usuarios del server\n12. Enviar notificaciones\n13. Salir\n")
            
            #Opcion para cerrar sesion
            if opcion =="1" and cliente != None:
                cliente.cerrar_sesion()
                #EnLinea == True
                cliente == None
                xmpp.disconnect()
                menu = False
                

            # opcion para eliminar 
            elif opcion == "2" :#and cliente != None:
                args.jid = input("Ingrese el usuario a eliminar: ")
                xmpp = eliminar_account(args.jid,args.password)
                xmpp.connect()
                xmpp.process(forever=False)

            #opcion para agregar contactos al roster 
            elif opcion == "4":
                usuario = input("Ingrese la cuenta del usuario a agregar: ")
                #nombre = input("Ingresa el nombre del usuario: ")
                xmpp = agregar_contacto(args.jid, args.password, usuario)
                xmpp.connect()
                xmpp.process(forever = False)
       
      
            # Opcion de enviar mensaje DISCLAIMER: NO RECIBE MENSAJES):
            elif opcion=="6":                
                args.to = input("Ingrese el usuario del destinatario a quien desea enviar un mensaje ")
                if args.message is None:
                    args.message = input("Escriba su mensaje: ")
                xmpp =Cliente(args.jid,args.password,args.to,args.message, "")
                xmpp.connect()
                xmpp.process(forever=False)


            #Mensaje de presencia personalizado
            elif opcion=="9":
                mensajePresencia = input("Ingrese su mensaje de presencia: ")
                xmpp = Cliente(args.jid,args.password,"", "", mensajePresencia)
                xmpp.connect()
                xmpp.process(forever=False)


            #SALIR
            elif opcion == "13":
                menu = False
                print("Gracias por visitarnos hoy")
