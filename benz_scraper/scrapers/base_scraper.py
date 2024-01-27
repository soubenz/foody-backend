from math import floor
import re
from playwright.sync_api import sync_playwright
import time
from pydantic import BaseModel
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from loguru import logger
from playwright_stealth import stealth_sync
from benz_scraper.utils import debug_delay, dump_items_to_json, parse_date, slight_delay

import dateparser




class BaseScraper:
    
    def __init__(self, playwright):
        self.browser = playwright.chromium.launch(headless=True)
        context = self.browser.new_context()
        page = context.new_page()
        stealth_sync(page)
        self.page = page
        logger.info("browser ready")
        
    def consent_cookies(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        button = self.page.locator('//form').nth(1)
        button.click()
        time.sleep(2)
        logger.info("consent given")


    def navigate(self, url):
        self.page.goto(url)
        slight_delay()
        logger.info("Page is loaded")
    
    def close(self):
        self.browser.close()
