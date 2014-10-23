import re
import subprocess


def mapDrive (drive, path):
    status = subprocess.check_output("net use")
    exp = r'OK\s+' + drive
    if re.search(exp, status, re.IGNORECASE):
        return True
    else:
        subprocess.call ("net use %s /delete" % drive)
        subprocess.call ("net use %s %s" % (drive, path))
        return False


                         
