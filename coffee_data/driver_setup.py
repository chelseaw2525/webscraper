from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import socket
import threading
import os

class handler:
    def __init__(self, chrome_path, chrome_driver_path, target):

        self.chrome_path = chrome_path
        self.chrome_driver_path = chrome_driver_path

        url = target
        free_port = self.find_available_port()
        self.launch_chrome_with_remote_debugging(free_port, url)
        self.driver = self.setup_webdriver(free_port)

    def find_available_port(self):
        #get local port number through temporary socket, bind it to an ephemeral port, then close the socket.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def launch_chrome_with_remote_debugging(self, port, url):
        def open_chrome():
            chrome_cmd = f"{self.chrome_path} --remote-debugging-port={port} --user-data-dir= {url}"
            os.system(chrome_cmd)

        chrome_thread = threading.Thread(target=open_chrome)
        chrome_thread.start()

    def setup_webdriver(self, port):
        #init driver to chrome browser w/ remote debugging enabled on specified port
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        driver = webdriver.Chrome(executable_path=self.chrome_driver_path, options=chrome_options)
        return driver
    
    def quit(self):
        print("Closing the browser...")
        self.driver.close()
        self.driver.quit()

    def send_prompt(self, prompt, location):
        #types message into box
        input_box = WebDriverWait(self.driver, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='"+ location +"'']")))
        #input_box = self.driver.find_element(by=By.XPATH, value='//textarea[contains(@placeholder,'+ location +')]')
        self.driver.execute_script(f"arguments[0].value = '{prompt}';", input_box)
        input_box.send_keys(Keys.RETURN)
        input_box.submit()



