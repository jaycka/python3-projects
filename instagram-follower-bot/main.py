import os
import time
import math

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

CHROME_DRIVER_PATH = os.environ.get('chrome_driver_path')
USERNAME = os.environ.get('instagram_username')
PASSWORD = os.environ.get('instagram_password')

instagram_login = 'https://www.instagram.com/'
similar_account = input('Please enter similar account name: ')
instagram_follower_page = f'https://www.instagram.com/{similar_account}/followers/'


class InstaFollower:
    def __init__(self, path: str):
        service = Service(executable_path=path)
        self.driver = webdriver.Chrome(service=service)
        self.follows_count = 0

    def login(self):
        self.driver.get(url=instagram_login)
        time.sleep(2)
        user_name_field = self.driver.find_element(By.NAME, 'username')
        user_name_field.click()
        user_name_field.send_keys(USERNAME)
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.click()
        password_field.send_keys(PASSWORD)
        time.sleep(1)
        password_field.send_keys(Keys.ENTER)
        time.sleep(5)

    def find_followers(self, url: str):
        self.driver.get(url=url)
        time.sleep(2)

    def follow(self):
        follower_count = int(self.driver.find_elements(By.CLASS_NAME, '_ac2a')[1].get_attribute('title').replace(',',''))
        scroll_number = math.ceil(follower_count/12)-1
        scroll_window = self.driver.find_element(By.CLASS_NAME, '_aano')

        for _ in range(scroll_number):
            follows_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'div.x1dm5mii div._aacl')[-12:]
            for follow in follows_buttons:
                try:
                    follow.click()
                except selenium.common.exceptions.ElementClickInterceptedException:
                    self.driver.find_element(By.CLASS_NAME, '_a9_1').click()
                    pass
                else:
                    self.follows_count += 1
                finally:
                    time.sleep(1)

            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', scroll_window)
            print(f'Followed {self.follows_count}')
            time.sleep(2)


if __name__ =='__main__':
    driver = InstaFollower(path=CHROME_DRIVER_PATH)
    driver.login()
    driver.find_followers(url=instagram_follower_page)
    driver.follow()
    driver.driver.quit()
