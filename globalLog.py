# -*-conding:utf-8-*-
import errno
import logging
import logging.config
import os


def get_logger(name='root'):
    conf_log = os.path.abspath(os.getcwd() + "/resource/logger_config.ini")
    logging.config.fileConfig(conf_log, disable_existing_loggers=False)
    return logging.getLogger(name)


def mkdir_p(path):
    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


class MakeFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False,
                 atTime=None):
        mkdir_p(os.path.dirname(filename))
        logging.handlers.TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay,
                                                           utc, atTime)


log = get_logger(__name__)
