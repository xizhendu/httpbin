import re
import os
import logging
from logging.handlers import TimedRotatingFileHandler


# Log
def service_logger(app_name):
    if not os.path.exists("logs"):
        os.mkdir(os.path.join(os.getcwd(), 'logs'))
    if not os.path.exists("logs/{0}".format(app_name)):
        os.mkdir(os.path.join(os.getcwd(), "logs/{0}".format(app_name)))

    logger = logging.getLogger('werkzeug')
    handler = TimedRotatingFileHandler(filename=os.path.join(os.getcwd(),
                                                             "logs/{0}".format(app_name),
                                                             "{0}.log".format(app_name)
                                                             ),
                                       when='midnight', backupCount=30, encoding='utf-8'
                                       )
    handler.suffix = '%Y-%m-%d.log'
    handler.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}.log')
    logger.addHandler(handler)
    return logger
