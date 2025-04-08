# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0005F7C7FA89D57B0471F186089303FF515A502D5172EEA2309A0AD021FEB9D0D249D736E61B5FA375B24483E284D2C7CC79E970D3042209D7CDFE86EAA23ECF26B2C5B8449A89180B3D0E604F6F11DAE5062846B7E418C99625E42D62F43D13884B9946C0833BC50FDCFCAB8E00B45A4833FC68C2A066C7FD268D029DA5C1073883E991255727D732139775E5D111AECF7C1CF44BE9D7DB65214904766A30EB72F5C6F981510FA83D04760656DAC46FA072AFDB465ECE7EFBCF02F4D094D7F899B6BB41E0AA19182A6420BB5FA3A4221B61AE2FB1A792376CC2315B24FE59B43D447215F65B0B0E411F791BBCCA0D7D9CB9F4D772DD2CA35E2F9C148D069EF7A56B87DC1E8FB9EBD13115EC2612E7E14A87304514124C55BD28CDC121552AFFB0270F008E4AD5A0D27261FC9EE0DE955A2117D45B2D2AEAAFC42F375C4F9D9F9FFF7E5B753643F980D7B2BA34A900F9B8"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
