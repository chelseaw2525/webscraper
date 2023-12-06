 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
from google.oauth2.service_account import Credentials
import time

import traceback

scopes = ['https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file("C:\\Users\\bookw\\Downloads\\liquid-receiver.json") #change to user
creds = creds.with_scopes(scopes)
client = gspread.authorize(credentials=creds)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options)

sheet_name = "" #insert target sheet here
sheet = client.open(sheet_name)
worksheet = sheet.get_worksheet(0)
wait = WebDriverWait(driver, 0.2)

print("can see sheet")

def update_worksheet_cell(cell, value):
    worksheet.update(cell, value)
    time.sleep(1)

result = ""

for row in range(238,281):
    print(f"Processing row {row}")
    cell = f"{chr(ord('A'))}{row}"
    term = worksheet.acell(cell).value

    lookup = f"{chr(ord('E'))}{row}"
    target = worksheet.acell(lookup).value

    print(term)
    time.sleep(1)

    try:
        #if term == None:
        driver.get(target)
        time.sleep(30)
        #update_worksheet_cell(cell, "done")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

print("process finished!!!!!!!!!!")
driver.quit()
 
