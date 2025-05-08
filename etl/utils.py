import logging

logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_logger(name):
    logger = logging.getLogger(name)
    return logger