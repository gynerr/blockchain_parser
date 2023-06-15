url = 'https://etherscan.io/txs?block=17450530'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_driver_path = 'G:\chromedriver\chromedriver.exe'
s = Service(executable_path=chrome_driver_path)

# Установка параметров браузера
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в безголовом режиме (без отображения окна браузера)
chrome_options.add_argument("--disable-gpu")  # Отключение GPU (для повышения производительности)
chrome_options.add_argument(("--disable-blink-features=AutomatioControlled"))

# Установка пути к ChromeDriver (загрузите ChromeDriver согласно версии вашего Chrome)


# Создание экземпляра браузера
driver = webdriver.Chrome(service=s)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {'source':
                                                                     '''
                                                                     delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array
                                                                     delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise
                                                                     delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol
                                                                     delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object
                                                                     delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy
                                                                     '''})
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
try:
    driver.maximize_window()
    driver.get(url)
    # # Ожидание полной загрузки страницы
    wait = WebDriverWait(driver, 36)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print(driver.page_source)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

# # Применение необходимых манипуляций (включение JavaScript и куки)
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#
# # Переход на страницу
# driver.get(url)
#
# # Ожидание полной загрузки страницы

# cookies = driver.get_cookies()
# print(cookies)
# # Проверка успешного доступа к странице
# page_title = driver.title
# driver.refresh()
# print(driver.title)
# print("Заголовок страницы:", page_title)

# Закрытие браузера
# driver.quit()
# response = requests.get(url)
# print(response.text)
