
# standard
from sys import argv
from socket import error as socketerror

# Project Hydra
from MySQLSetup import Hydra_rendertask, transaction, KILLED, READY, STARTED
from Connections import TCPConnection
from Questions import KillCurrentJobQuestion
from LoggingSetup import logger

def sendKillQuestion(renderhost, newStatus=KILLED):
    """Tries to kill the current task running on the renderhost. Returns True
    if successful, otherwise False"""

    logger.debug ('kill job on %s' % renderhost)
    connection = TCPConnection(hostname=renderhost)
    answer = connection.getAnswer(
                            KillCurrentJobQuestion(newStatus))

    logger.debug("child killed: %s" % answer.childKilled)
    
    if not answer.childKilled:
        logger.debug("%r tried to kill its job but failed for some reason." 
                        % renderhost)
    
    return answer.childKilled
    
def killJob(job_id):
    """Kills every task associated with job_id. Killed tasks have status code 
    'K'. If a task was already started, an a kill request is sent to the host 
    running it.
    @return: False if no errors while killing started tasks, else True"""
    
    # mark all of the Ready tasks as Killed
    with transaction() as t:
        t.cur.execute("""update Hydra_rendertask set status = 'K' 
                        where job_id = '%d' and status = 'R'""" % job_id)
    
    # get hostnames for tasks that were already started
    tuples = None # @UnusedVariable
    with transaction() as t:
        t.cur.execute("""select host from Hydra_rendertask 
                        where job_id = '%d' and status = 'S'""" % job_id)
        tuples = t.cur.fetchall()
        
    # make flat list out of single-element tuples fetched from db
    hosts = [t for (t,) in tuples]
    
    # send a kill request to each host, note if any failures occurred
    error = False
    for host in hosts:
        try:
            error = error or not sendKillQuestion(host)
        except socketerror:
            logger.debug("There was a problem communicating with {:s}"
                         .format(host))
            error = True
    
    return error

def resurrectJob(job_id):
    """Resurrects job with the given id. Tasks marked 'K' or 'F' will have 
    their data cleared and their statuses set to 'R'"""
    
    with transaction() as t:
        t.cur.execute("""update Hydra_rendertask 
                        set status = 'R' 
                        where job_id = '%d' and 
                        status = 'K' or status = 'F'""" % job_id)

def killTask(task_id):
    """Kills the task with the specified id. If the task has been started, a 
    kill request is sent to the node running it.
    @return: True if there were no errors killing the task, else False."""
    
    [task] = Hydra_rendertask.fetch("where id = '%d'" % task_id)
    if task.status == READY:
        task.status = KILLED
        with transaction() as t:
            task.update(t)
        # if we reach this point: transaction successful, no exception raised
        return True
    elif task.status == STARTED:
        killed = sendKillQuestion(renderhost = task.host, newStatus = KILLED)
        # if we reach this point: TCPconnection successful, no exception raised
        return killed
    return False

def resurrectTask(task_id, ignoreStarted = False):
    """Resurrects the task with the specified id. 
    @return: True if there was an error, such as when the user tries to 
             resurrect a task that is marked as Started, else False."""
    
    [task] = Hydra_rendertask.fetch("where id = '%d'" % task_id)
    if (
            task.status == 'K' or task.status == 'F' or 
            (task.status == 'S' and ignoreStarted == True)
        ):
        task.status = 'R'
        task.host = None
        task.startTime = None
        task.endTime = None
    else:
        return True

    with transaction() as t:
        task.update(t)
    
    return False

if __name__ == '__main__':
    if len(argv) == 3:
        cmd, job_id = argv[1], int(argv[2])
        if cmd == 'kill':
            killJob(job_id)
        elif cmd == 'resurrect':
            resurrectJob(job_id)
    else:
        print "Command line args: ['kill' or 'resurrect'] [job_id]"
