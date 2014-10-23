import os

PORT = 8765
HOSTNAME = "localhost" # for testing on a single machine
#HOSTNAME = "154-01"    # for testing on another machine
MANYBYTES = 1 << 20
BASELOGDIR = r'c:\Hydra\logs'
RENDERLOGDIR = os.path.join( BASELOGDIR, 'render' )
