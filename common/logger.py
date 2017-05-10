import logging
logger = logging.getLogger()
fhandler = logging.FileHandler(filename='output/mylog.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)
logging.Logger.disabled=True
