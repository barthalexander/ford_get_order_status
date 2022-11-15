from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from send_request import send_request
from send_pushover import send_pushover

def send_selenium(config):


    # driver = webdriver.Chrome(service=service)

    # make chrome log requests
    capabilities = DesiredCapabilities.CHROME
    capabilities['goog:loggingPrefs'] = {'browser': 'ALL', 'driver': 'ALL', "performance": "ALL"}

    driver = webdriver.Remote(
       desired_capabilities=capabilities,
       command_executor=config["DEFAULT"]["SELENIUM_ENDPOINT"],
       options=webdriver.ChromeOptions(),
    )

    try:
        driver.get("https://www.ford.de/hilfe/fahrzeug-ueberblick?vin=" + config["FORD"]["VIN"])
        
        sleep(5)  # wait for the requests to take place
        
        driver.find_element(By.ID, "cookieBannerAcceptBtn").click()

        sleep(3)  # wait for the requests to take place

        username = driver.find_element(By.ID, "username")
        username.send_keys(config["FORD"]["USERNAME"])

        password = driver.find_element(By.ID, "password")
        password.send_keys(config["FORD"]["PASSWORD"])

        password.send_keys(Keys.RETURN)
        
        sleep(10)  # wait for the requests to take place

        logs = driver.get_log('performance')

        driver.close()
        driver.quit()
        return logs
    
    except:
        driver.close()
        driver.quit()
        return ""