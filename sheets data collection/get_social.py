
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

driver = webdriver.Chrome()
sheet_name = "" #insert sheet name here
sheet = client.open(sheet_name)
worksheet = sheet.get_worksheet(0)
wait = WebDriverWait(driver, 0.5)

print("can see sheet")

def update_worksheet_cell(cell, result):
    target = worksheet.acell(cell).value
    if target is None:
        worksheet.update(cell, result)  # Update cell at column with result


for row in range(0, 3420):

    link = worksheet.acell(f"{chr(ord('B'))}{row}").value
    title = worksheet.acell(f"{chr(ord('A'))}{row}").value
    curr_time = time.strftime("%H:%M:%S",time.localtime())
    time.sleep(1)
    try:
        
        print(f"{curr_time}, processing row {row} with {title}")
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

        discord_links = [link.get_attribute('href') for link in links if link.get_attribute('href') is not None and 'discord.com' in link.get_attribute('href')]
        if len(discord_links) > 0:
            discord = discord_links[0]
            update_worksheet_cell(f"{chr(ord('E'))}{row}",discord)
        
        print("updated socials")

    except Exception as e:
        print(f"Error occurred: {e}")

print("process finished!!!!!!!!!!")
driver.quit()