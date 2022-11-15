import configparser
import logging

from send_request import send_request
from send_pushover import send_pushover
from send_selenium import send_selenium

from time import sleep
import json

config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(level=config["DEFAULT"]["DEBUG_LEVEL"])

logging.info("Getting Logs")
logs = send_selenium(config)

logging.info("Parsing Logs")
for entry in logs:
   if "order-status" in entry["message"]:
      if "eyJ" in entry["message"]:
         log = json.loads(entry["message"])["message"]
         try:
            token = log["params"]["request"]["headers"]["Auth-Token"]
         except:
            print("failure print headers")

logging.info("Wait 120s")
sleep(120)  # wait for the requests to take place

logging.info("Try to get order-status")
for i in range(0,10):
   try:
      response = send_request(token)
      send_pushover(config, response['result'])
      break
   except:
      logging.info("Token not valid. Please wait 30s")
      sleep(30)
      continue
