from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("https://discordapp.com/login")
time.sleep(20)
for i in range (0, 1000):
	try:
		element = driver.find_element(By.CSS_SELECTOR, "[aria-label='Message @polaris']")
		element.send_keys(Keys.ARROW_UP)
		element = driver.find_element(By.CSS_SELECTOR, "div[role='textbox']")
		element.click()
		for i in range(0, 50):
			element.send_keys(Keys.BACKSPACE)
			element.send_keys(Keys.DELETE)
		element.send_keys(Keys.ENTER)
		time.sleep(0.5)
		button = driver.find_element(By.XPATH, "//button[contains(@class, 'button-ejjZWC lookFilled-1H2Jvj colorRed-2VFhM4 sizeMedium-2oH5mg grow-2T4nbg')]")
		button.send_keys(Keys.ENTER)
		time.sleep(1)
	except Exception as e: 
		print(f"An error occurred")
		
