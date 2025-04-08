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
    browser.add_cookie({"name": "MUSIC_U", "value": "007050E11C50860A491153386E70FA53DD610FCDE8FC99B4D7E4EA688EE1C6F5BFF83AA85B7CECE833149D89F3852F78B26EC59880C480D419D759CCB861E745DE464805FDA3DC675526ED31EBE2AF770C6D2AF57D52BB602BBC4273429E938CB22800DBE68776928D16FD06A342429129AD4D9F1DD373D335D4ACFEC3C798CD84447C5AE8F38AF855F7C336DBFD3E54684E841B9A74F858A340E5E558462886B3608EC8922388701BE2018E44A7260609D8FDFA5B9064FEC599757DA3E7B870D88B089C4ADAE81C58ED9591DED082A8673D1DAAD433BA2EFDB03092DFAF7CF11701E1508E691E75176986BA40EEB385E06C4105AC1123B7C48DBE31564DA5A93F9CFEFB754504DE74A7F8ED42A2E7D1B561533D9C502543D9B2F0056E4DF80A064AAB207E0C006AF4F1B135517565E2F25314610D60596351A0D2CE550B2C2C678E83F277F56CE6110A6372BDFC04DC8E"})
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
