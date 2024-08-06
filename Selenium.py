import random
import time

import undetected_chromedriver
from undetected_chromedriver import Chrome
from bs4 import BeautifulSoup
from loguru import logger
import pyautogui as pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


chrome_driver_path = 'G:\chromedriver\chromedriver.exe'
s = Service(executable_path=chrome_driver_path)
screen_width, screen_height = pyautogui.size()

def move_mouse_randomly():
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    pyautogui.moveTo(x, y, duration=0.5)


# Установка пути к ChromeDriver (загрузите ChromeDriver согласно версии вашего Chrome)
profile_path = r'C:\Users\User\AppData\Local\Google\Chrome\User Data'


def pasrse_page_by_selenium(url):
    s = Service(executable_path=chrome_driver_path)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    # chrome_options.add_argument("--headless")  # Запуск в безголовом режиме (без отображения окна браузера)
    # chrome_options.add_argument("--disable-gpu")  # Отключение GPU (для повышения производительности)
    # chrome_options.add_argument('--user-data-dir=' + profile_path)
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    # driver = webdriver.Chrome(service=s, options=chrome_options)
    driver = undetected_chromedriver.Chrome()
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {'source':
    #                                                                      '''
    #                                                                      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array
    #                                                                      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise
    #                                                                      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol
    #                                                                      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object
    #                                                                      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy
    #                                                                      '''})
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # stealth(driver,
    #         languages=["en-US", "en"],
    #         vendor="Google Inc.",
    #         platform="Win64",
    #         webgl_vendor="Intel Inc.",
    #         renderer="Intel Iris OpenGL Engine",
    #         fix_hairline=True,
    #         )
    try:
        driver.maximize_window()
        driver.get(url)
        # Ожидание полной загрузки страницы
        # wait = WebDriverWait(driver, 36)
        time.sleep(8)
        response = driver.page_source
        response_soup = BeautifulSoup(response, 'lxml')
        if response_soup.title.text == 'Just a moment...':
            logger.info('Проверка соединения!')
            response = driver.page_source
            response_soup = BeautifulSoup(response, 'lxml')
            response_table = response_soup.find('body').find('table')
            logger.info('Проверка пройдена!')
        elif response_soup.title.text == 'Ethereum BlockChain Explorer | Maintenance Mode':
            driver.refresh()
            response = driver.page_source
    except Exception as ex:
        logger.error("Exception")
    finally:
        driver.close()
        driver.quit()
    return response

# # Проверка успешного доступа к странице
# page_title = driver.title
# driver.refresh()
