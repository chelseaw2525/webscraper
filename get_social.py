
from selenium import webdriver
from selenium.webdriver.common.by import By
import gspread
from google.oauth2.service_account import Credentials
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import traceback
import re

def find_this(driver, partial_link_text):
    xpath_expression = "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]".format(partial_link_text.lower())
    elements = driver.find_elements(By.XPATH, xpath_expression)
    return elements

scopes = ['https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file("C:\\Users\\bookw\\Downloads\\liquid-receiver-386602-04d443fa11c8.json")
creds = creds.with_scopes(scopes)
client = gspread.authorize(credentials=creds)

driver = webdriver.Chrome()

sheet_name = "0 - Blockchain Data"
sheet = client.open(sheet_name)
worksheet = sheet.get_worksheet(0)
wait = WebDriverWait(driver, 5)

print("can see sheet")

#def update_worksheet_cell(cell, value):
#    worksheet.update(cell, value)

def update_worksheet_cell(cell, result):
    target = worksheet.acell(cell).value
    if target is None:
        worksheet.update(cell, result)  # Update cell at column with result


for row in range(577, 3085):

    link = worksheet.acell(f"{chr(ord('D'))}{row}").value
    title = worksheet.acell(f"{chr(ord('A'))}{row}").value
    
    try:

        print(f"Processing row {row} with {title}")
        driver.get(link)
        wait.until(EC.presence_of_all_elements_located)

        links = driver.find_elements(By.TAG_NAME, 'a')
        print("links scanned")

        twitter_links = [link.get_attribute('href') for link in links if link.get_attribute('href') is not None and 'twitter.com' in link.get_attribute('href')]
        if len(twitter_links) > 0:
            twitter = twitter_links[0]
            update_worksheet_cell(f"{chr(ord('E'))}{row}",twitter)
        
        linkedin_links = [link.get_attribute('href') for link in links if link.get_attribute('href') is not None and 'linkedin.com' in link.get_attribute('href')]
        if len(linkedin_links) > 0:
            linkedin = linkedin_links[0]
            update_worksheet_cell(f"{chr(ord('F'))}{row}",linkedin)
        
        discord_links = [link.get_attribute('href') for link in links if link.get_attribute('href') is not None and 'discord.gg' in link.get_attribute('href')]
        if len(discord_links) > 0:
            discord = discord_links[0]
            update_worksheet_cell(f"{chr(ord('G'))}{row}",discord)
        
        print("checked for socials")
        time.sleep(2)

    except Exception as e:
        print(f"Error occurred: {e}")

print("process finished!!!!!!!!!!")
driver.quit()
