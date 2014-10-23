import re

from MySQLSetup import transaction, Hydra_rendertask

badTasks = Hydra_rendertask.fetch ("where command like '%-p''%'")
print len(badTasks)
for task in badTasks:
    task.command = task.command.replace("'-p'", "'-proj'")
    task.status = 'R'
    task.startTime = None
    task.endTime = None
    task.exitCode = None
    #task.command = re.sub (r"PyQt4.QtCore.QString\(u(.*)\)", r'\1', task.command)
    with transaction () as t:
        task.update (t)
        
    
