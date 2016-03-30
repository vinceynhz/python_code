# Logger levels
DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3
CRITICAL = 4

# Logger formatting constants
FORMAT = '[%(levelname)8s %(asctime)s][%(threadName)-10s][%(filename)15s:%(funcName)-10s] %(message)s'
DATEFMT = '%Y%d%m %I%M.%S'

def log(logger, lvl, msg):
    ''' Wrapper of a logger object to use in multithreaded apps '''
    if logger is not None:
        return {
            DEBUG : logger.debug,
            INFO : logger.info,
            WARNING : logger.warning,
            ERROR : logger.error,
            CRITICAL : logger.critical
        }[lvl](msg)

def printif(verbose, *pargs):
    ''' Print if a condition is met; the way I use this is:

    def some_method(*pargs, verbose):
        # add some code
        printif(verbose, "message to be printed")
        # more code

    That way, the module doesn't add the decision everytime and let the user
    decide whether messages should be printed or not '''
    if(verbose): print(*pargs)
