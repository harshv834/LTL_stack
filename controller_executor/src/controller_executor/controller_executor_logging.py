"""
logging for this package temporarily. PIPE to ros later?
Modified from LTLMoP
"""

import logging
import ConfigParser
import sys, os
import time

loggerLevel = {"controller": "DEBUG", \
               "input_manager": "DEBUG", \
               "output_manager": "DEBUG",\
               "prop_monitor": "DEBUG",\
               "setup_execution": "DEBUG",\
               "region_operations": "DEBUG"}

def setupLogging(loggerLevel=None):
    # Set up loggers for printing error messages
    class ColorLogFormatter(logging.Formatter):
        def __init__(self, *args, **kwds):
            super(ColorLogFormatter, self).__init__(*args, **kwds)
            self.plain_formatter = logging.Formatter("%(asctime)s.%(msecs)3d %(levelname)5s [ %(module)s ] %(message)s", "%H:%M:%S")
            self.debug_formatter = logging.Formatter("%(asctime)s.%(msecs)3d %(levelname)5s [ %(module)s ] %(message)s (line %(lineno)s)", "%H:%M:%S")
            self.detailed_formatter = logging.Formatter("%(asctime)s.%(msecs)3d %(levelname)5s[ %(module)s ] %(message)s  (%(pathname)s, line %(lineno)s)", "%H:%M:%S")

        def colorize(self, level, string):
            if sys.platform in ['win32', 'cygwin']:
                # Message with color is not yet supported in Windows
                return string

            else:
                colors = {'ERROR': 91, 'WARNING': 93, 'INFO': 97, 'DEBUG': 94, 'Level 1': 100, 'Level 2': 105, 'Level 4': 104, 'Level 6': 102, 'Level 8': 101}
                return "\033[{0}m{1}\033[0m".format(colors[level], string)

        def format(self, record):
            if record.levelname == "INFO":
                precolor = self.plain_formatter.format(record)
            elif record.levelname == "DEBUG":
                precolor = self.debug_formatter.format(record)
            else:
                precolor = self.detailed_formatter.format(record)

            return self.colorize(record.levelname, precolor)

    loggers = {"controller": logging.getLogger("controller_logger"), \
               "input_manager": logging.getLogger("input_manager_logger"), \
               "output_manager": logging.getLogger("output_manager_logger"),\
               "prop_monitor": logging.getLogger("prop_monitor_logger"),\
               "setup_execution": logging.getLogger("setup_execution_logger"),\
               "region_operations": logging.getLogger("region_operations_logger")}

    h = logging.StreamHandler()
    f = ColorLogFormatter()
    h.setFormatter(f)
    for logger in loggers.values():
        if not logger.handlers:
            logger.addHandler(h)

    # also save to file
    # read from terminal: tail -f /var/log/syslog -f /var/tmp/contoller_logger.log
    for logger_name, logger in loggers.iteritems():
        h_file = logging.FileHandler('/var/tmp/'+logger_name+'_logger.log', mode='w')
        h_file.setFormatter(f)
        logger.addHandler(h_file)

    cfg = ConfigParser.ConfigParser()

    #try:
    #    cfg.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),"global.cfg"))
    #    loggerLevel = cfg.get("logging", "level").lower()
    #except:
    #    logging.warning("Could not parse global.cfg file; using defaults")
    #    loggerLevel = "info"

    for logger_name, logger in loggers.iteritems():
        if loggerLevel[logger_name].lower() == 'error':
            logger.setLevel(logging.ERROR)
        elif loggerLevel[logger_name].lower() == 'warning':
            logger.setLevel(logging.WARNING)
        elif loggerLevel[logger_name].lower() == 'info':
            logger.setLevel(logging.INFO)
        elif loggerLevel[logger_name].lower() == 'debug':
            logger.setLevel(logging.DEBUG)
        elif loggerLevel[logger_name].lower() == 'notset':
            #logger.setLevel(logging.NOTSET)
            # for some reason logging.NOTSET does not work
            logger.setLevel(int(1))
        else:
            logger.setLevel(int(loggerLevel[logger_name]))

# Choose the timer func with maximum accuracy for given platform
if sys.platform in ['win32', 'cygwin']:
    best_timer = time.clock
else:
    best_timer = time.time

# Set-up logging automatically on import
setupLogging(loggerLevel)