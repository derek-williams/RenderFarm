
from MySQLSetup import transaction, Hydra_rendernode
import Utils    
    
def unregister(host=None):
    """
    Removes the specified node from Hydra_rendernode table. If none provided,
    then it gets the host name of the current machine / configuration and
    removes that from the database. For example, if the current machine's
    computer name is FOO and the DNS extension listed in hydraSettings.cfg is
    .xyz, then the host to be deleted is FOO.xyz
    """
    
    if not host:
        host = Utils.myHostName()
    
    [node] = Hydra_rendernode.fetch("where host = '%s'" % host)
    if node:
        with transaction() as t:
            t.cur.execute("delete from Hydra_rendernode where host = '%s'" % host)
        return True
    
    return False