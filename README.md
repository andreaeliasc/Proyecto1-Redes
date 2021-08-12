# XMPP Client

# XMPP Client Implementation - Network Project

This is a project about the implementation and correct XMPP Protocol use. The project objective is 
stick to the standards of a known and open protocol. Understand the asynchronous programming foundations 
required to adhere to the development needs in networks.

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/XMPP_logo.svg/220px-XMPP_logo.svg.png">

## About XMPP Protocol

XMPP (Extensible Messaging and Presence Protocol) is a communication protocol for message-oriented middleware 
based on XML (Extensible Markup Language). XML is is markup language that defines a set of rules for encoding 
documents in a format that is both human-readable and machine-readable. XMPP enables the exchange of structured 
yet extensible data between any two or more network entitiies. Originally named Jabber, it twas developed by the 
eponymous open-source community in 1999 for near real-time instant messaging, presence information, and contact 
list maintenance.

## Programing Language
- **Python** - 3.7.0v

##Functionality Video
https://youtu.be/zgr_7JHmnC4


## Dependencies
These are the dependences or libraries that use the client

```python
import sys
import logging
from getpass import getpass
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
import threading
```

## How to Run
First, you need to clone this repository
```bash
https://github.com/andreaeliasc/Proyecto1-Redes
```

Then you need to run the next command to execute the XMPP Client

```bash
python ./Proyecto.py
```
or
```bash
python3 ./Proyecto.py
```

# Project Content and Functions
The next content and functions was implemented in this XMPP Cliennt. 
There is a small explanation about the operation of each functionality

- **User Registration** 
This functionality do the new user registration with a new user with a domain 
(user@domain) and a password. This use pluging to band register XEP_0077. It
create an object Register that do the register process.

- **User Login** 
This functionality do the login for a user registered previously, and 
a password. It create an object Client that will handle other actions when 
an user is loged in.

- **User Logout** 
This functionality do the logout for a user that is loged in. It applies a 
sleekxmpp library method that handle the disconnect event to log out. 

- **Delete User Account** 
This functionality do the unregister for a user that is loged in. It 
construct an IQ Stanza to use remove query about register account. You have 
to introduce your user (user@domain) to delete your account

- **Add User to Roster** 
This functionality add an user that we wish to subscribe. It require the user 
that the client wish to add. It add a user to client roster with a SliXMPP 
method called 'send_presence_subscription'. It sends a petition to the user and 
it decide if accept or not the subscription.

- **Send Presence Message** 
This functionality send a presence message that is a Message Stanza with 
an internal tag that notificate user receptor, and it is a message that is
showed everytime that our client is connected.


## Difficulties
During the development of this project i got to experience difficulties with
Python exactly with some of the dependecies and libraries needed to be able
to use XMPP, also i got to stuggle a lot with the sintaxis cause i could'nt 
understand it completely, even though these project wasn't completed the way i 
wished i got to learn some stuff.

## What did i learned?
I got to learn that timing is important maybe if i had started before the 
result would have been better, also got to learn a lot about the xmpp sintaxis
even though not completely. Another big lesson i have learned from this is to 
read documentation about libraries and optimize my time.


## Implemented Characteristics
Login
Register
LogOut
Send Message
Add Contact
Delete Contact



## References
- https://slixmpp.readthedocs.io/en/slix-1.6.0/getting_started/echobot.html
- https://slixmpp.readthedocs.io/en/latest/
- [XMPP: The Definitive Guide By Saint, P. Smith, K & Troncon, R.](https://oriolrius.cat/blog/wp-content/uploads/2009/10/Oreilly.XMPP.The.Definitive.Guide.May.2009.pdf)
- [XMPP - Extensions reference](https://xmpp.org/)
- [Client Tester](https://jwchat.org/)