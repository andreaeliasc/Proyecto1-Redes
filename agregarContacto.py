
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

class agregar_contacto(slixmpp.ClientXMPP):

    def __init__(self, jid, contraseña, amic):
        slixmpp.ClientXMPP.__init__(self, jid, contraseña)
        self.add_event_handler("session_start", self.start)
        self.user = jid
        self.toAdd = amic
        

    async def start(self, event):
        self.send_presence()
        self.get_roster()
        try:
            self.send_presence_subscription(pto=self.toAdd)
        except IqTimeout:
            print("No se pudo agregar contacto")
        
        self.disconnect() 
