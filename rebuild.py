import os
import sys
import itertools
import subprocess

for target in sys.argv[1:]:

        target = target.replace ('-setup', '')
        target = target.replace ('.py', '')
        print "target", target
        folderFormat = target + '-dist-%03d' 

        for i in itertools.count(1):
            folderName = folderFormat % i
            print folderName
            if os.path.isdir (folderName):
                continue
            break

        cmd = ['python', target + '-setup.py', 'py2exe', '--includes', 'sip', '-d', folderName]
        print cmd
        subprocess.call (cmd)

