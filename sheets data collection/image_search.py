from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

driver = webdriver.Chrome()
sheet_name = "" #insert sheet name here
sheet = client.open(sheet_name)
print(sheet_name)
worksheet = sheet.get_worksheet(0)

print("can see sheet")

for row in range(2, 52):
    print(f"Processing row {row}")
    cell = f"{chr(ord('D'))}{row}"
    term = worksheet.acell(cell).value
    print(term)
    time.sleep(1)

    try:
        if term != "":
            driver.get('https://www.google.com/imghp?hl=en&ogbl')
            search_input = driver.find_element(By.NAME, 'q')
            search_input.clear()
            search_input.send_keys("\""+ term + " ecosystem\" map")
            search_input.send_keys(Keys.ENTER)

            wait = WebDriverWait(driver, 5)
            search_result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rg_i')))
            link_element = search_result.find_element(By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[2]')
            top_result_link = link_element.get_attribute('href')
            
            worksheet.update(f"{chr(ord('E'))}{row}", top_result_link)
            time.sleep(1.5)

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

print("process finished!!!!!!!!!!")
driver.quit()
 
