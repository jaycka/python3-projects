from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


def driver_setup(url: str) -> webdriver:
    chrome_driver_path = r"C:\Users\Eric\PycharmProjects\chromedriver_win32\chromedriver.exe"
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    return driver


def check_balance(driver: webdriver) -> int:
    return int(driver.find_element(By.ID, 'money').text.replace(',', ''))


def get_highest_available(driver: webdriver, balance: int):
    available_purchase = driver.find_elements(By.CSS_SELECTOR, '#store b')
    available_to_buy = []
    for i in available_purchase[:-1]:
        price = int(i.text.split('-')[-1].strip().replace(',', ''))
        if price <= balance:
            available_to_buy.append(i.text.split('-')[0].strip())
    to_buy = driver.find_element(By.ID, f'buy{available_to_buy[-1]}')
    to_buy.click()
    print(f'Bought {available_to_buy[-1]}')


if __name__ == '__main__':
    driver = driver_setup('http://orteil.dashnet.org/experiments/cookie/')
    cookie_button = driver.find_element(By.ID, 'cookie')
    start = time.time()
    timeout = time.time() + 5
    while time.time() < start + 60 * 5:
        cookie_button.click()
        if time.time() >= timeout:
            timeout = time.time() + 5
            get_highest_available(driver, check_balance(driver))
    print(driver.find_element(By.ID, 'cps').text)
    driver.quit()
