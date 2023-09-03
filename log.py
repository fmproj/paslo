import logging

def getLogger(name):
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.StreamHandler()
        ],
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    return logging.getLogger(name)