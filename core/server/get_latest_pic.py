
import asyncio
from pathlib import Path
from time import sleep
from weakref import proxy
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re
import subprocess
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

# playwright install
# playwright install --with-deps
# playwright install-deps 

class GetLatestPic:
    def __init__(self,tempFileName:str):
        self.tempFileName = tempFileName

    async def get_latest_pic_from_url_async(self,url:str,width:int,height:int) -> Path:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            # await page.set_viewport_size({
            #     "width": width,
            #     "height": height
            # })
            await page.goto(url,wait_until="domcontentloaded")
            await asyncio.sleep(10)
            await page.screenshot(path=f"{self.tempFileName}")
            await browser.close()

        return Path(self.tempFileName)
    
    def get_latest_pic_from_url(self,url:str,width:int,height:int) -> Path:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            # await page.set_viewport_size({
            #     "width": width,
            #     "height": height
            # })
            page.goto(url,wait_until="domcontentloaded")
            asyncio.sleep(10)
            page.screenshot(path=f"{self.tempFileName}")
            browser.close()

        return Path(self.tempFileName)
    
    def get_latest_pic_from_url_selenium(self,url:str,width:int,height:int) -> Path:
        options = Options()
        options.add_argument("--headless")
        
        # プロキシ環境の場合、no_proxy=localhost,127.0.0.1の設定も必要
        options.add_argument("--proxy-server=http://192.168.11.10:3128")

        driver = webdriver.Chrome(options=options)
        driver.set_window_size(width,height)
        driver.get(url)

        sleep(10)

        driver.save_screenshot(f"selenium_{self.tempFileName}")
        driver.quit()

        return Path(f"selenium_{self.tempFileName}")