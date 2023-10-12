 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
from google.oauth2.service_account import Credentials
import time
from selenium.common.exceptions import StaleElementReferenceException
import re
from bs4 import BeautifulSoup
import traceback

scopes = ['https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file("C:\\Users\\bookw\\Downloads\\liquid-receiver-386602-04d443fa11c8.json")
creds = creds.with_scopes(scopes)
client = gspread.authorize(credentials=creds)

driver = webdriver.Chrome()

sheet_name = "0 - Blockchain Data"
sheet = client.open(sheet_name)
worksheet = sheet.get_worksheet(0)

print("can see sheet")

for row in range(1246, 4185):
    print(f"Processing row {row}")
    cell = f"{chr(ord('A'))}{row}"
    term = worksheet.acell(cell).value
    print(term)
    time.sleep(2)

    try:
        if term != "":
            driver.get('https://www.google.com/')
            search_input = driver.find_element(By.NAME, 'q')
            search_input.clear()
            search_input.send_keys(term + " blockchain linkedin")
            search_input.send_keys(Keys.ENTER)
            wait = WebDriverWait(driver, 5)
            search_result = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yuRUbf')))
            link_element = search_result.find_element(By.TAG_NAME, 'a')
            top_result_link = link_element.get_attribute('href')
            worksheet.update(f"{chr(ord('l'))}{row}", top_result_link)
            time.sleep(6)

            driver.get('https://www.google.com/')
            search_input = driver.find_element(By.NAME, 'q')
            search_input.clear()
            search_input.send_keys(term + " blockchain twitter")
            search_input.send_keys(Keys.ENTER)
            wait = WebDriverWait(driver, 5)
            search_result = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yuRUbf')))
            link_element = search_result.find_element(By.TAG_NAME, 'a')
            top_result_link = link_element.get_attribute('href')
            worksheet.update(f"{chr(ord('n'))}{row}", top_result_link)
            time.sleep(6)

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

print("process finished!!!!!!!!!!")
driver.quit()
 
