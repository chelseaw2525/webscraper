import time
from selenium import webdriver

from driver_setup import handler

chrome_driver_path = r"C:\webdrivers\chromedriver.exe"
chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
target_url = r"https://squareup.com/dashboard/sales/transactions"
driver = handler(chrome_path, chrome_driver_path, target_url)

email = "apps@dedicatedmkt.com"
password = ".354FubWNNXG8Ej"


element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Email address']")))
element.click()
element.send_keys(email)
element.send_keys(Keys.ENTER)
time.sleep(1)
print("email entered")

element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Password']")))
element.click()
element.send_keys(password)
element.send_keys(Keys.ENTER)
time.sleep(1)
print("password entered")

element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Export']")))
element.click()
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Generate Transactions CSV']")))
element.click()
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Download Transactions CSV']")))
element.click()
print("download time")

driver.quit()
