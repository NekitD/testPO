from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

def setup_driver():
    s_options = Options()
    s_options.add_argument('--no-sandbox')
    s_options.add_argument('--disable-dev-shm-usage')
    s_options.add_argument('--ignore-certificate-errors')
    
    s_options.add_argument('--headless')
    
    s_service = Service('/usr/bin/chromedriver')



    driver = webdriver.Chrome(service=s_service, options=s_options)
    driver.implicitly_wait(10)
    return driver


def login_openbmc():
    driver = setup_driver()
    try:
        driver.get('https://10.0.2.15')
        
        username_field = driver.find_element(By.ID, 'username')  
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        username_field.send_keys('root')
        password_field.send_keys('0penBmc')
        login_button.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'dashboard'))
        )
        return 0
        
    finally:
        driver.quit()
        return 1
    

def test_login_succes():
    assert login_openbmc() == 0

