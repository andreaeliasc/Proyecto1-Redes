#Andrea Estefania Elias Cobar 
#17048


import logging
from getpass import getpass #libreria para ocultar contraseña
from argparse import ArgumentParser
from os import name
import slixmpp
from slixmpp.exceptions import XMPPError
from slixmpp.xmlstream import ET, tostring
from slixmpp import Iq
from slixmpp.exceptions import IqError, IqTimeout


#Clase que nos permite agregar un contacto al roster

class agregar_contacto(slixmpp.ClientXMPP):

### Aqui se hace el proceso para agrega un usuario al roster
    def __init__(self, jid, contraseña, amic):
        slixmpp.ClientXMPP.__init__(self, jid, contraseña)   
        self.add_event_handler("session_start", self.start)
        self.user = jid
        self.toAdd = amic
        

### Aqui se hace el proceso para agrega un usuario al roster
    def start(self, event):
        self.send_presence()
        self.get_roster()
        try:
            self.send_presence_subscription(pto=self.toAdd) ### El metodo de slixmpp se encarga de enviar el request de solicitud al usuario dest
        except IqTimeout:
            print("No se pudo agregar contacto")
        
        self.disconnect() 








    

