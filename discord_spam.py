from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("https://discordapp.com/login")
time.sleep(30)
for i in range (0, 10000):
	try:
		element = driver.find_element(By.CSS_SELECTOR, "[aria-label='Message @andrewhc']")
		element.click()
		element.send_keys('get spammed lol')
		element.send_keys(Keys.ENTER)
		time.sleep(0.5)
	except Exception as e: 
		print(f"An error occurred")
		
