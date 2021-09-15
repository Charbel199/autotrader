import logging

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    filename='./debug.log', level=logging.DEBUG)
logging.info('Started logging ...')
