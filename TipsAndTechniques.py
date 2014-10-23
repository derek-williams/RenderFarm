"""Miscellaneous pieces of useful code."""

from LoggingSetup import logger
import subprocess
import os
import traceback

def toRunMaya( ):

    command = [r"c:\Program Files\Autodesk\Maya2011\bin\Render.exe",
               "-help",
               ]

    # it's easier to supply the "words" on a command line as individual strings
    # rather than glueing them together into one big string.
    # the subprocess module's functions let you do either.
    return subprocess.call (command)

def withOutputToFile( filename, command ):
    "run a command, sending output to a file"

    logger.debug( 'writing log file %s', filename )

    with file( filename, 'w' ) as f:
        f.write( "Launching command %r\n\n" % command )
        f.flush( )
        # the 'with' statement closes f if there's an error
        return subprocess.call( command,
                                stdout = f,
                                stderr = subprocess.STDOUT,
                                )
    
def listRenderers(  ):

    command = [
               r"c:\Program Files\Autodesk\Maya2011\bin\Render.exe",
               "-listRenderers",
               ]

    tempDir = os.getenv( 'TMP')
    logFile = os.path.join( tempDir, 'logfile1.txt' )
    return withOutputToFile( logFile, command )

def missingArgument(  ):

    command = [r"c:\Program Files\Autodesk\Maya2011\bin\Render.exe",
               
               ]

    tempDir = os.getenv( 'TMP')
    logFile = os.path.join( tempDir, 'logfile2.txt' )
    return withOutputToFile( logFile, command )

def commandNameError(  ):

    command = ["cmd",
               "/c",
               r"c:\Program Files\Autodesk\Maya2011\bin\Render.exeeeeeeee",
                "-help"               
               ]
    # using cmd /c to run the command starts a new shell. That way if the program name is wrong, the shell
    # will complain about it, but the subprocess.call won't fail. Which it would, if you simply passed it a bad
    # command to launch.
    

    tempDir = os.getenv( 'TMP')
    logFile = os.path.join( tempDir, 'logfile3.txt' )
    return withOutputToFile( logFile, command )

def actualMayaRender( ):
    command = [
           r'c:\program files\autodesk\maya2011\bin\render.exe',
           
           '-mr:v', '5',
           # we need verbosity 5 to see where the
           # render went and to get progress during long renders
           
           r'c:\users\gladstein\desktop\chair2.ma',
           ]
    logFileName = r'c:\temp\test.log.txt'
    log = file( logFileName, 'w' )

    try:
        log.write( 'Hydra log file %s on %s\n' % ( logFileName, os.environ['COMPUTERNAME'] ) )
        # identify the log file in the log file itself, so if it gets emailed you know where it came from.
        
        log.write( 'Command is %s\n\n' % ( command ) )
        # put the command arguments in the log file

        log.flush( )
        
        return subprocess.call( command, stdout=log, stderr=subprocess.STDOUT )
    except Exception, e:
        traceback.print_exc( e, log )
        raise
    finally:
        log.close( )



if __name__ == '__main__':

    logger.debug( 'return code %s', toRunMaya( ) )

    logger.debug( 'return code %s', listRenderers( ) )
    
    logger.debug( 'return code %s', missingArgument( ) )
    
    logger.debug( 'return code %s', commandNameError( ) )

    logger.debug( 'return code %s', actualMayaRender( ) )
    
    
