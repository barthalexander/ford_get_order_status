from auth import AuthClient
from send_request import send_request
from send_pushover import send_pushover
import configparser
from time import sleep
import logging
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root

config = configparser.ConfigParser()
config.read(ROOT_DIR + '/config.ini')

logging.basicConfig(level=config["DEFAULT"]["DEBUG_LEVEL"])


logging.info('Try to get token')
login = AuthClient(config)
token = login.get_user_access_token(config["FORD"]["USERNAME"], config["FORD"]["PASSWORD"])
logging.debug('Token: ' + str(token))

logging.info('Try to order-status')
for i in range(0,10):
   try:
      response = send_request(config, token['access_token'])
      logging.debug('Response: ' + str(response))
      
      send_pushover(config, response['result'])
      break
   except:
      logging.info('we have to wait for a valid call')
      continue