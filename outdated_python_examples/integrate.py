from selenium import webdriver
from selenium.webdriver.common.by import By
import gspread
from google.oauth2.service_account import Credentials
import time
from selenium.common.exceptions import StaleElementReferenceException


scopes = ['https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file("C:\\Users\\bookw\\Downloads\\liquid-receiver.json") #change to user
creds = creds.with_scopes(scopes)
client = gspread.authorize(credentials=creds)

driver = webdriver.Chrome()

sheet_name = "chainset"
sheet = client.open(sheet_name)
worksheet = sheet.get_worksheet(0)
time.sleep(1)

print("can see sheet")

def update_worksheet_cell(cell, value):
    worksheet.update(cell, value)
    time.sleep(1)

for row in range(1424, 1823):
    cell = f"{chr(ord('B'))}{row}"
    link = worksheet.acell(cell).value
    time.sleep(1)
    print(link)
    
    try:
        driver.get(link)
        site = driver.find_element(By.LINK_TEXT, "Website").get_attribute("href")
        twits = driver.find_elements(By.LINK_TEXT, "Twitter")
        ans = twits[1].get_attribute("href") if len(twits) >= 2 else None
        
        update_worksheet_cell(f"{chr(ord('C'))}{row}", site)  # Update column C with site_href
        update_worksheet_cell(f"{chr(ord('D'))}{row}", ans)   # Update column D with twit_href
        
        print("updated")
    except Exception as e:
        print(f"Error occurred: {e}")

print("process finished!!!!!!!!!!")
driver.quit()
