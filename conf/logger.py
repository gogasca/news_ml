import logging.config


class Singleton(type):
    """

    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


class LoggerManager(object):
    """

    """
    __metaclass__ = Singleton

    _loggers = {}

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def getLogger(name='___app__', logging_file='', filemode='w+', **kwargs):
        """

        :param name:
        :param logging_file:
        :param filemode:
        :param kwargs:
        :return:
        """
        # Define timezone
        if filemode:
            logging.basicConfig(filename=logging_file,
                                filemode=filemode,
                                level=logging.INFO,
                                format='%(asctime)s.%(msecs).03d %('
                                       'levelname)s %(message)s',
                                datefmt='%m/%d/%Y %H:%M:%S')
        else:
            return logging.getLogger()

        if not name:
            return logging.getLogger()
        elif name not in LoggerManager._loggers.keys():
            LoggerManager._loggers[name] = logging.getLogger(str(name))
        return LoggerManager._loggers[name]
