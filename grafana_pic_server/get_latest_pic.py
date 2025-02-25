
from pathlib import Path
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

# playwright install
# playwright install --with-deps
# playwright install-deps 

class GetLatestPic:
    def __init__(self,tempFileName:str):
        self.tempFileName = tempFileName

    def get_latest_pic_from_url_selenium(self,url:str,width:int,height:int) -> Path:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        
        # プロキシ環境の場合、no_proxy=localhost,127.0.0.1の設定が必要
        # options.add_argument("--proxy-server=http://192.168.11.10:3128")

        driver = webdriver.Chrome(options=options)
        driver.set_window_size(width,height)
        driver.get(url)

        # xpath = "/html/body/div/div/div[1]/div/div/main/div[3]/div/div[1]/div/div/svg"
        # WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH,xpath)))
        sleep(10)

        driver.save_screenshot(f"selenium_{self.tempFileName}")
        driver.quit()

        return Path(f"selenium_{self.tempFileName}")