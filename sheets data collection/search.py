from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
from google.oauth2.service_account import Credentials
import traceback
from selenium.webdriver.support import Options
import time

scopes = ['https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file("C:\\Users\\bookw\\Downloads\\liquid-receiver.json")
creds = creds.with_scopes(scopes)
client = gspread.authorize(credentials=creds)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options) 

sheet_name = "test"
sheet = client.open(sheet_name)
print(sheet_name)
worksheet = sheet.get_worksheet(0)
wait = WebDriverWait(driver, 0.2)

print("can see sheet")
time.sleep(1)

values = worksheet.col_values(1)
results = []

for i in range(0, len(values)):
    term = values[i]
    print(term)

    try:
        if term != "":
            driver.get(f"https://www.google.com/search?q={term}")
            search_result = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yuRUbf')))
            link_element = search_result.find_element(By.TAG_NAME, 'a')
            top_result_link = link_element.get_attribute('href') 
            results.append(top_result_link)      

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

cell_list = worksheet.range('b1:b20')

for i in range(0, len(cell_list)):
    cell_list[i].value = results[i]

worksheet.update_cells(cell_list)

print("process finished!!!!!!!!!!")
driver.quit()
