from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

TWITTER_ID = os.environ.get('twitter_id')
TWITTER_PASSWORD = os.environ.get('twitter_password')
PROMISED_UP = 100
PROMISED_DOWN = 1000
chrome_driver_path = r"C:\Users\Eric\PycharmProjects\chromedriver_win32\chromedriver.exe"
speed_test = 'https://www.speedtest.net/'
twitter = 'https://twitter.com/i/flow/login'


class InternetSpeedTwitterBot:
    def __init__(self):
        service = Service(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get(url=speed_test)
        time.sleep(10)
        start_button = self.driver.find_element(By.CLASS_NAME, 'start-text')
        start_button.click()
        time.sleep(60)
        results = self.driver.find_elements(By.CLASS_NAME, 'result-data-large')
        self.down = float(results[0].text)
        self.up = float(results[1].text)

    def tweet_at_provider(self):
        self.driver.get(url=twitter)
        time.sleep(2)

        user_name_field = self.driver.find_element(By.CLASS_NAME, 'r-30o5oe')
        user_name_field.send_keys(TWITTER_ID)
        user_name_field.send_keys(Keys.ENTER)
        time.sleep(2)

        password_field = self.driver.find_element(By.XPATH,
                                                  '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password_field.click()
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.send_keys(Keys.ENTER)
        time.sleep(5)

        click_to_edit_field = self.driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block')
        click_to_edit_field.click()
        edit_field = self.driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-ltr')
        edit_field.send_keys(
            f'Hey @Comcast, why is my internet speed {self.down}down/{self.up}up when I pay 80 bucks per month for 1000down/100up?')
        tweet_button = self.driver.find_element(By.XPATH,
                                                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[3]/div/span/span')
        tweet_button.click()



driver = InternetSpeedTwitterBot()
driver.get_internet_speed()
driver.tweet_at_provider()
driver.driver.quit()
