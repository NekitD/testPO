from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pytest

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
        return True
        
    except:
        return False
    
    finally:
        driver.quit()


def account_block_openbmc():
    driver = setup_driver()
    max_attempts = 5 
    
    try:
        for attempt in range(1, max_attempts + 1):
            print(f"Попытка {attempt}/{max_attempts}")
            
            driver.get('https://127.0.0.1:2443/login')
            time.sleep(10)
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'username'))
                )
            except TimeoutException:
                print("Форма входа не загрузилась")
                return False
            
            try:
                username_field = driver.find_element(By.ID, 'username')  
                password_field = driver.find_element(By.ID, 'password')
                login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
                
                username_field.clear()
                password_field.clear()
                username_field.send_keys('root')
                password_field.send_keys('wrong_password_' + str(attempt)) 
                login_button.click()
                
                time.sleep(2)
                
            except NoSuchElementException:
                print("Не удалось найти элементы формы")
                return False
            
            try:
                fail_message = driver.find_element(By.XPATH, '//*[contains(text(), "error") or contains(text(), "invalid") or contains(text(), "incorrect") or contains(text(), "невер")]')
                print(f"Неудачный вход: {fail_message.text}")
            except:
                print("Неудачный вход (без сообщения)")
            
            if "login" in driver.current_url.lower():
                print("Всё ещё на странице входа")
            else:
                print("Ушли со страницы входа - что-то пошло не так")
                break
        
        print("\nПробуем войти с правильным паролем после блокировки...")
        driver.get('https://127.0.0.1:2443/login')
        time.sleep(3)
        
        try:
            username_field = driver.find_element(By.ID, 'username')  
            password_field = driver.find_element(By.ID, 'password')
            login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
            
            username_field.clear()
            password_field.clear()
            username_field.send_keys('root')
            password_field.send_keys('0penBmc')
            login_button.click()
            
            time.sleep(3)
            
        except NoSuchElementException:
            print("Не удалось найти форму после блокировки")
            return 1
        
        current_url = driver.current_url
        
        if "login" in current_url.lower():
            try:
                block_message = driver.find_element(By.XPATH, '//*[contains(text(), "lock") or contains(text(), "block") or contains(text(), "temporarily") or contains(text(), "wait") or contains(text(), "заблок")]')
                print(f"Аккаунт заблокирован: {block_message.text}")
                return True
            except:
                print("Аккаунт заблокирован (без сообщения)")
                return True
        else:
            print("Аккаунт НЕ заблокирован - вошли успешно")
            return False  
            
    except Exception as e:
        print(f"ОШИБКА: {e}")
        return False


def inventory_show():
    driver = setup_driver()
    try:
        driver.get("https://127.0.0.1:2443/login")
        time.sleep(3)
        
        driver.find_element(By.ID, 'username').send_keys('root')
        driver.find_element(By.ID, 'password').send_keys('0penBmc')
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(3)

        url = "https://127.0.0.1:2443/#/hardware-status/inventory"
        
        inventory_found = False
        try:
            driver.get(url)
            time.sleep(3)
                
            inventory_elements = driver.find_elements(By.XPATH, 
                '//*[contains(text(), "CPU") or contains(text(), "Processor") or '
                'contains(text(), "Memory") or contains(text(), "RAM") or '
                'contains(text(), "DIMM") or contains(text(), "Hardware") or '
                'contains(text(), "Inventory") or contains(text(), "System")]'
            )
                
            if inventory_elements:
                print(f"Найдены элементы инвентаризации на {url}:")
                for elem in inventory_elements[:5]:
                    print(f"   - {elem.text}")
                inventory_found = True           
        except Exception as e:
            print(f"Ошибка при проверке {url}: {e}")

        
        if not inventory_found:
            print("Поиск инвентаризации в текущем интерфейсе...")
            inventory_buttons = driver.find_elements(By.XPATH,
                '//*[contains(text(), "Inventory") or contains(text(), "Hardware") or '
                    'contains(text(), "System") or contains(text(), "Components")]'
            )
            
            if inventory_buttons:
                print("Найдены кнопки инвентаризации:")
                for btn in inventory_buttons:
                    print(f"   - {btn.text}")
                    try:
                        btn.click()
                        time.sleep(3)
                        inventory_found = True
                        break
                    except:
                        continue
        
        return inventory_found
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def check_power_on_logs():
    driver = setup_driver()
    try:
        driver.get("https://127.0.0.1:2443/login")
        time.sleep(10)
        driver.find_element(By.ID, 'username').send_keys('root')
        driver.find_element(By.ID, 'password').send_keys('0penBmc')
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(10)

        driver.get("https://127.0.0.1:2443/?next=/login#/operations/server-power-operations")
        time.sleep(10)
        power_on_button = driver.find_element(By.XPATH, '//button[contains(text(), "Power on")]')
        power_on_button.click()

        time.sleep(10)
        

        driver.get("https://127.0.0.1:2443/?next=/login#/logs/event-logs")
        time.sleep(10)

        power_logs = driver.find_elements(By.XPATH, '//*[contains(text(), "Power on") or contains(text(), "error") or contains(text(), "Error")]')
        
        if power_logs:
            print("В логах найдена запись о включении питания")
            for log in power_logs[:2]:
                print(f"   - {log.text}")
            return True
        else:
            print("В логах нет записи о включении питания")
            return False

    except Exception as e:
        print(f"Ошибка: {e}")
        return False

#---------------------------------------------------------------------------------------

def test_login_success():
    assert login_openbmc('root', '0penBmc') == True

@pytest.mark.xfail(reason="WRONG LOGIN AND PASSWORD")
def test_login_fail():
    assert login_openbmc('nikita', 'gastello') == True

def test_account_block():
    assert account_block_openbmc() == True


def test_inventory_show():
    assert inventory_show() == True

def test_logs_show():
    assert check_power_on_logs() == True