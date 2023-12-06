from selenium import webdriver
from selenium.webdriver.common.by import By
import gspread
from google.oauth2.service_account import Credentials
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC


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

def update_worksheet_cell(cell, result):
    target = worksheet.acell(cell).value
    if target is None:
        worksheet.update(cell, result)  # Update cell at column with result

values = worksheet.col_values(2)
results = []
print(f"first value is {values[0]}")
time.sleep(1)

#values to look for
search_val = "" 
alt_val = ""

for i in range(1837, len(values)):
    term = values[i]
    print(term)
    curr_time = time.strftime("%H:%M:%S",time.localtime())
    
    try:
        print(f"{curr_time}, processing row {i+1}")
        driver.get(term)
        wait.until(EC.presence_of_all_elements_located)

        #links = driver.find_elements(By.TAG_NAME, 'a')
        #print("links scanned")

        try:
            search = driver.find_element(By.PARTIAL_LINK_TEXT, search_val).get_attribute("href")
            update_worksheet_cell(f"{chr(ord('H'))}{i+1}", search)
        except Exception as e:
            print(f"Error search: {e}")

        try:
            alt = driver.find_element(By.PARTIAL_LINK_TEXT, alt_val).get_attribute("href")
            update_worksheet_cell(f"{chr(ord('I'))}{i+1}", alt)
        except Exception as e:
            print(f"Error alt: {e}")
            
        print("updated")

    except Exception as e:
        print(f"Error occurred: {e}")

driver.quit()