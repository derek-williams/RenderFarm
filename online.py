import os

import LoggingSetup
import Utils

from MySQLSetup import Hydra_rendernode, OFFLINE, IDLE, transaction

with transaction () as t:
    [thisNode] = Hydra_rendernode.fetch( "where host = '%s'" % Utils.myHostName( ) )
    if thisNode.status == OFFLINE:
        thisNode.status = IDLE
        thisNode.update(t)
    
