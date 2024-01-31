import asyncio
import time
from benz_scraper.db import create_restaurant
from benz_scraper.py_models import RestaurantMetadata, RestaurantReview
from benz_scraper.scrapers.base_scraper import BaseScraper
from benz_scraper.utils import determine_pricing, slight_delay
from math import floor
import re
from playwright.sync_api import sync_playwright
import time
from pydantic import BaseModel
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from loguru import logger
from playwright_stealth import stealth_sync
from benz_scraper.utils import debug_delay, dump_items_to_json, parse_date, slight_delay
from datetime import datetime, timedelta
import dateparser


class RestaurantsScraper(BaseScraper):
    
    def __init__(self,  city, category, limit=10, headless=True):
        super().__init__ (headless=headless)
        self.city = city
        self.category = category
        self.limit = limit
        self.search_term = f"{category} restaurant in {city}"
        self.url = "https://www.google.com/maps"
        
    async def prepare_restuarants(self):

        # await self.page.goto("https://www.google.com/maps")
        await self.page.keyboard.type(self.search_term, delay=300)
        await self.page.keyboard.press('Enter')
        self.restaurents = self.page.locator("a.hfpxzc")
        await asyncio.sleep(2)
        
    # async def get_metadata(self):
        # nb_reviews = await self.page.locator('div.F7nice > span:nth-child(2) > span > span').inner_text()
        # pricing = await self.page.locator('span.mgr77e').all_inner_texts()
        # av_stars = await self.page.locator('span.ceNzKf').get_attribute("aria-label")
        # av_stars = await self.page.locator('div.F7nice > span:nth-child(1) > span:nth-child(1)').inner_text()
        # title = await self.page.locator('h1.DUwDvf > span.a5H0ec').inner_text()
        # category = await self.page.locator('button.DkEaL ').inner_text()
        # self.true_nb = int(nb_reviews.strip("()"))
        # slight_delay()
        # self.metadata = RestaurantMetadata(category=category, name=title, nb_reviews=nb_reviews, average_rating=av_stars)
        # print(category, title, nb_reviews, av_stars, self.true_nb)
        
    async def scrape_restaurents(self, review_idx):
        result_elem = self.restaurents.nth(review_idx)
        name = await self.restaurents.nth(review_idx).get_attribute("aria-label")
        await result_elem.click()
        time.sleep(2)
        try:
            _pricing = await self.page.locator('span.mgr77e').all_inner_texts()
            pricing = determine_pricing(_pricing)
        except PlaywrightTimeoutError:
            pricing = None
            logger.warning("no pricing")    
        # av_stars = await self.page.locator('span.ceNzKf').get_attribute("aria-label")
        try:
            av_stars = await self.page.locator('div.F7nice > span:nth-child(1) > span:nth-child(1)').inner_text(timeout=1500)
            av_stars = float(av_stars.replace(",", "."))
        except PlaywrightTimeoutError: 
            av_stars = None
            logger.warning("no average stars")

        try:
            category = await self.page.locator('button.DkEaL ').inner_text(timeout=1500)
        except PlaywrightTimeoutError:
            logger.warning(f"Error getting category")
            category = self.category

        try:
            url = await self.restaurents.nth(review_idx).get_attribute("href", timeout=1500)
        except PlaywrightTimeoutError:
            url = None
            logger.warning(f"Error getting URL")

        try:
            description = await self.page.locator('div.PYvSYb ').inner_text(timeout=1500)
        except PlaywrightTimeoutError:
            description = None
            logger.warning(f"Error getting description")

        try:
            address = await self.page.locator('div.Io6YTe.fontBodyMedium.kR99db').nth(0).inner_text(timeout=1500)
        except PlaywrightTimeoutError:
            address = None
            logger.warning(f"Error getting address")

        try:
            cover_img = await self.page.locator('div.RZ66Rb.FgCUCc > button > img').get_attribute("src", timeout=3000)
        except PlaywrightTimeoutError:
            cover_img = None
            logger.warning(f"Error getting cover image")
        await create_restaurant(name, url, pricing, av_stars, category, url,  address, description,cover_img)
        # tournament = await Tournament.create(name="New Tournament")
        return name, pricing, av_stars, category, url, description, address, cover_img
       
       

    def clean_stars(self,stars_text):
        return stars_text.split(" stars")[0]
    
    async def close(self):
        await self.browser.close()
        
        
    async def run(self):
        async with async_playwright() as playwright:
            await self.init(playwright)
            await self.navigate(self.url)
            await self.consent_cookies()
            time.sleep(5)
            await self.prepare_restuarants()
            scrapped_item = 0
            items = []
            try:
                while scrapped_item < self.limit:
                    await asyncio.sleep(3)
                    await self.page.mouse.wheel(0, 100000)
                    for _ in range(5):
                        if scrapped_item >= self.limit:
                            break
                        item = await self.scrape_restaurents(scrapped_item)
                        print(item)
                        scrapped_item += 1
                    # debug_delay()
 
                
            except Exception as e:
                print(e)
                raise e
            finally:
                await self.close()
