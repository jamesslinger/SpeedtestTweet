## DESKTOP VERSION ##
import os
import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

PROMISED_UP = 100
PROMISED_DOWN = 700
TWITTER_USER = "@Bird_App_User_"
TWITTER_PW = os.environ.get("TWITTER_PW")
TWITTER_URL = "https://twitter.com/i/flow/login"
SPEEDTEST_URL = "https://www.speedtest.net/"
SERVICE = Service("D:/Coding/chromedriver.exe")
WEBDRIVER = webdriver.Chrome(service=SERVICE)


class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = WEBDRIVER
        self.promised_up = PROMISED_UP
        self.promised_down = PROMISED_DOWN
        self.current_down = None
        self.current_up = None

    def get_internet_speed(self):
        self.driver.get(SPEEDTEST_URL)
        time.sleep(3)
        try:
            cookies_alert = self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
            cookies_alert.click()
        except Exception:
            print("Popup not found, moving on...")
        time.sleep(3)
        start_btn = self.driver.find_element(By.CLASS_NAME, "start-text")
        start_btn.click()
        time.sleep(40)
        try:
            decline_popup = self.driver.find_element(By.XPATH,
            '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/div/div[2]/a')
            decline_popup.click()
        except Exception:
            print("Popup not found, moving on...")
        time.sleep(3)
        self.current_down = float(self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text)
        print(f"Download: {self.current_down}Mbps")
        self.current_up = float(self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)
        print(f"Upload: {self.current_up}Mbps")

    def tweet_my_provider(self):
        self.driver.get(TWITTER_URL)
        time.sleep(2)
        input_username = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        time.sleep(2)
        input_username.click()
        input_username.send_keys(TWITTER_USER)
        time.sleep(2)
        next_btn = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span')
        time.sleep(2)
        next_btn.click()
        time.sleep(2)
        input_password = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        time.sleep(2)
        input_password.send_keys(TWITTER_PW)
        time.sleep(2)
        login_btn = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
        login_btn.click()
        time.sleep(5)
        try:
            notification_popup = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div')
            notification_popup.click()
        except Exception:
            print("Popup not found, moving on...")
        time.sleep(2)
        tweet_btn = self.driver.find_element(By.XPATH,
        '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a')
        tweet_btn.click()
        time.sleep(3)
        type_tweet = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div/div/div/div/div')
        type_tweet.click()
        time.sleep(3)
        type_tweet.send_keys(f"Hey Internet Service Provider, my internet speed isn't as promised."
                             f"\nIt's currently;"
                             f"\n- Down: {self.current_down}Mbps, Up: {self.current_up}Mbps"
                             f"\nwhen it should be at least;"
                             f"\n- Down: {self.promised_down}Mbps, Up: {self.promised_up}Mbps"
                             f"\nWhat gives?")
        time.sleep(2)
        send_tweet = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]')
        send_tweet.click()
        print("Tweet sent. All done. Goodbye.")


auto_checker = InternetSpeedTwitterBot()
auto_checker.get_internet_speed()

if auto_checker.current_down < auto_checker.promised_down or auto_checker.current_up < auto_checker.promised_up:
    print("Slow speeds, tweeting ISP!")
    auto_checker.tweet_my_provider()
else:
    print("Speed's good today! Ending application. Goodbye.")
