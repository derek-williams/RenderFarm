
# Project Hydra
from MySQLSetup import Hydra_rendertask, Hydra_job, transaction
from LoggingSetup import logger

def prioritizeJob(job_id, priority):
    
    with transaction() as t:
        t.cur.execute("""update Hydra_job
                        set priority = '%d'
                        where id = '%d'""" % (priority, job_id))
        t.cur.execute("""update Hydra_rendertask
                        set priority = '%d'
                        where job_id = '%d'""" % (priority, job_id))





