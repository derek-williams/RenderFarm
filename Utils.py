"""Miscellaneous pieces of useful code."""
import ConfigParser
import os
import Constants
import itertools

def myHostName( ):
    "this computer's host name in the RenderHost table"
    # open config file
    config = ConfigParser.RawConfigParser ()
    config.read ("C:/Hydra/hydraSettings.cfg")
    
    domain = config.get (section="network", option="dnsDomainExtension")
    
    return os.getenv( 'COMPUTERNAME' ) + domain

def flanged (name):
    return name.startswith ('__') and name.endswith ('__')

def nonFlanged (name):
    return not flanged (name)

# receive all bytes from a socket, with no buffer size limit jive
def sockRecvAll (sock):
    # generator to recieve strings from socket, will return
    # empty strings (forever) upon EOF
    receivedStrings  = (sock.recv (Constants.MANYBYTES)
                        for i in itertools.count (0))
    # concatenate the nonempty ones
    return ''.join (itertools.takewhile (len, receivedStrings))

def flushOut (f):
    "flush and sync a file to disk"
    f.flush()
    os.fsync(f.fileno())
