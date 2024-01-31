from math import floor
import re
from playwright.sync_api import sync_playwright
import time
from pydantic import BaseModel
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from loguru import logger
from playwright_stealth import stealth_async
from tortoise import Tortoise
from benz_scraper.utils import debug_delay, dump_items_to_json, parse_date, slight_delay

import dateparser
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URI = os.environ.get("DATABASE_URI")


class BaseScraper:
    
    def __init__(self,  headless=True):
        self.headless = headless
        # self.playwright = playwright
        
    async def init(self, playwright):
        self.browser = await playwright.chromium.launch(headless=self.headless)
        context = await self.browser.new_context(locale='en-GB')
        page = await context.new_page()
        await stealth_async(page)
        self.page = page
        self.page.set_default_timeout(2000)
        logger.info("browser ready")
        await Tortoise.init(
        db_url=DATABASE_URI,
        modules={'models': ['benz_scraper.models']}
        )
        # Generate the schema
        logger.info("DB connection ready")
    
        
    async def consent_cookies(self):
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        button = self.page.locator('//form').nth(1)
        await button.click()
        time.sleep(2)
        logger.info("consent given")


    async def navigate(self, url):
        await self.page.goto(url)
        slight_delay()
        logger.info("Page is loaded")
    
    async def close(self):
        await self.browser.close()
        await Tortoise.close_connections()
