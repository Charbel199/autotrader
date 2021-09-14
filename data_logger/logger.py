import logging

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    filename='./debug.log', level=logging.INFO)
logging.info('Started logging ...')