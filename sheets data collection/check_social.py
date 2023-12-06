from selenium import webdriver
from selenium.webdriver.common.by import By
import gspread
from google.oauth2.service_account import Credentials
import time
from selenium.common.exceptions import StaleElementReferenceException

def find_this(driver, partial_link_text):
    xpath_expression = "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]".format(partial_link_text.lower())
    elements = driver.find_elements(By.XPATH, xpath_expression)
    return elements

scopes = ['https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file("C:\\Users\\bookw\\Downloads\\liquid-receiver-386602-04d443fa11c8.json")
creds = creds.with_scopes(scopes)
client = gspread.authorize(credentials=creds)

driver = webdriver.Chrome()

sheet_name = "chainset"
sheet = client.open(sheet_name)
worksheet = sheet.get_worksheet(0)

print("can see sheet")

def update_worksheet_cell(cell, value):
    worksheet.update(cell, value)
    time.sleep(0.8)

for row in range(3, 3085):
    cell = f"{chr(ord('c'))}{row}"
    link = worksheet.acell(cell).value
    print(f"Processing row {row}")
    
    try:
        print(link)
        driver.get(link)

        links = driver.find_elements(By.TAG_NAME, 'a')
        twitter_links = [link.get_attribute('href') for link in links if link.get_attribute('href') is not None and 'twitter.com' in link.get_attribute('href')]
        print("checked for twitter")
        linkedin_links = [link.get_attribute('href') for link in links if link.get_attribute('href') is not None and 'linkedin.com' in link.get_attribute('href')]
        print("checked for linkedin")
        discord_links = [link.get_attribute('href') for link in links if link.get_attribute('href') is not None and 'discord.gg' in link.get_attribute('href')]
        print("checked for discord")

        if len(linkedin_links) > 1 or len(twitter_links) > 1 or len(discord_links) > 1:
            update_worksheet_cell(f"{chr(ord('N'))}{row}", "TRUE") 
        
        print("updated")

    except Exception as e:
        print(f"Error occurred: {e}")

print("process finished!!!!!!!!!!")
driver.quit()
