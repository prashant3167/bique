# Import the required modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver

import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import sleep
import time


chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
)
driver = webdriver.Chrome(options=chrome_options)


def login_upwork():
    driver.get(
        "https://www.upwork.com/ab/ats-aas/api/profile-search/profiles?category_uid=531770282584862721&occupation_uid=1110580754793353216&page=2&subcategory_uid=531770282601639945"
    )
    wait = WebDriverWait(driver, 20)
    elem = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="login_username"]'))
    )
    #Add email here
    elem.send_keys("")

    elem = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="login_password_continue"]'))
    )
    elem.click()
    driver.implicitly_wait(15)
    sleep(10)
    elem = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="login_password"]'))
    )
    # sleep(30)
    #Add password here
    password = ""
    elem.send_keys(password)
    elem = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="login_control_continue"]'))
    )
    elem.click()
    sleep(5)


def get_info(page=1):
    driver.get(
        f"https://www.upwork.com/ab/ats-aas/api/profile-search/profiles?category_uid=531770282584862721&occupation_uid=1110580754793353216&page={page}&subcategory_uid=531770282601639945"
    )

    html = driver.execute_script(
        "return document.getElementsByTagName('pre')[0].innerText"
    )
    json_data = json.loads(html)
    return json_data
import requests
import json
reqUrl = "http://10.4.41.51:8000/ingest/clevertap"

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Content-Type": "application/json" 
}

def send_requests(data):
    for j,i in enumerate(data):
        print(j)
        payload = json.dumps(i)
        response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
        print(response.text)

login_upwork()
for i in range(11, 400):
    # page = input("Give page number: ")
    data = get_info(i)
    send_requests(data["results"]["profiles"])
    # print(data["results"]["profiles"])
