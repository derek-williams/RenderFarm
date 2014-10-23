
# standard
from sys import argv
from socket import error as socketerror

# 3rd party
from Connections import TCPConnection
from Questions import CMDQuestion

def sendRebootQuestion(renderhost):
    
    connection = TCPConnection(hostname=renderhost)
    answer = connection.getAnswer(CMDQuestion("shutdown /r /t 0"))
    return answer    

if __name__ == '__main__':
    if len(argv) == 2:
        host = argv[1]
        print sendRebootQuestion (host).output
    else:
        print ("Type the host name of a render node to reboot it, or type 'q'" 
               " to quit.")
        host = raw_input("Host to reboot: ")
        while host.lower() != 'q':
            try:
                print sendRebootQuestion(host).output
            except socketerror as err:
                print str(err)
                if err.errno == 11004:
                    print "Hostname could not be resolved to an address."
                print # newline
                    
            host = raw_input("Host to reboot: ")
            