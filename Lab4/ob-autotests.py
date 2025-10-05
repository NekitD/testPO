from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def set_driver():
    s_options = ChromiumOptions
    s_options.add_argument('--no-sandbox')
    s_options.add_argument('--disable-dev-shm-usage')
    s_options.add_argument('--ignore-certificate-errors')
    s_options.add_argument('--headless')

    driver = webdriver.Chrome(options=s_options)
    return driver
