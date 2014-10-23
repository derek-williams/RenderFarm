from MySQLSetup import Hydra_rendernode, Hydra_rendertask, transaction, IDLE, READY, STARTED, FINISHED
from LoggingSetup import logger

def unstick (taskID=None, newTaskStatus=READY,
             host=None, newHostStatus=IDLE):
    with transaction () as t:
        if taskID:
            [task] = Hydra_rendertask.fetch ("where id = %d" % taskID)

            # if the task is marked, say, CRASHED, leave the host name alone.
            # only READY would be confusing with a host named filled in. I think.
            if newTaskStatus == READY:
                task.host = None

            task.status = newTaskStatus
            task.startTime = None
            task.endTime = None
            task.update (t)
        if host:
            [host] = Hydra_rendernode.fetch ("where host = '%s'" % host)
            host.task_id = None
            host.status = newHostStatus
            host.update (t)
