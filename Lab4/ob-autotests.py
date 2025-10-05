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
    s_options.add_argument('--ignore-ssl-errors') 
    s_options.add_argument('--headless')
    
    s_service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=s_service, options=s_options)
    driver.implicitly_wait(10)
    return driver

def login_openbmc(user, password):
    driver = setup_driver()
    try:
        driver.get('https://127.0.0.1:2443')
        time.sleep(2)
        
        username_field = driver.find_element(By.ID, 'username')  
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        
        username_field.send_keys(user)
        password_field.send_keys(password)
        login_button.click()
        
        WebDriverWait(driver, 5).until(
            lambda driver: "/login" not in driver.current_url
        )
        return 0
        
    except:
        return 1
    
    finally:
        driver.quit()

def test_login_success():
    assert login_openbmc('root', '0penBmc') == 0


def test_login_fail():
    assert login_openbmc('nikita', 'gastello') == 1