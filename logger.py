import logging


LOG_FORMAT = '%(asctime)s [%(levelname)s] [%(funcName)s] - %(message)s'


logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)


def get_instance():
    return logging.getLogger('D.E.V.A')
