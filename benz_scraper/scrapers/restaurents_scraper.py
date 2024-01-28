




import time
from benz_scraper.models import RestaurantMetadata, RestaurantReview
from benz_scraper.scrapers.base_scraper import BaseScraper
from benz_scraper.utils import slight_delay
from math import floor
import re
from playwright.sync_api import sync_playwright
import time
from pydantic import BaseModel
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from loguru import logger
from playwright_stealth import stealth_sync
from benz_scraper.utils import debug_delay, dump_items_to_json, parse_date, slight_delay
from datetime import datetime, timedelta
import dateparser


class RestaurentsScraper(BaseScraper):
    def prepare_restuarents(self):
        self.page.keyboard.type("African restaurent in Paris", delay=100)
        self.page.keyboard.press('Enter')
        self.restaurents = self.page.locator("a.hfpxzc")
        time.sleep(2)
       
        
    def get_metadata(self):
        
        # nb_reviews = self.page.locator('div.jANrlb > div.fontBodySmall').inner_text()
        nb_reviews = self.page.locator('div.F7nice > span:nth-child(2) > span > span').inner_text()
        av_stars = self.page.locator('span.ceNzKf').get_attribute("aria-label")
        title = self.page.locator('h1.DUwDvf > span.a5H0ec').inner_text()
        category = self.page.locator('button.DkEaL ').inner_text()
        self.true_nb = int(nb_reviews.strip("()"))
        slight_delay()
        self.metadata = RestaurantMetadata(category=category, name=title, nb_reviews=nb_reviews, average_rating=av_stars)
        print(category, title, nb_reviews, av_stars, self.true_nb)
        
        
    def scrape_restaurents(self, review_idx):
        result_elem = self.restaurents.nth(review_idx)
        name = self.restaurents.nth(review_idx).get_attribute("aria-label")
        url = self.restaurents.nth(review_idx).get_attribute("href")
        details = result_elem.locator('div.W4Efsd > div.W4Efsd > span').all_inner_texts()
        print(name, url, details)
        return
        try:
            button_more = result_elem.locator('div.MyEned > span > button.w8nwRe').click(timeout=1500)
        except PlaywrightTimeoutError:
            pass
        try:
            text = result_elem.locator('//div[@class="MyEned"]/span[@class="wiI7pd"]').inner_text(timeout=1500)
        except PlaywrightTimeoutError:
            logger.warning("no text in review")
            text= None
        stars = result_elem.locator('//span[@class="kvMYJc"]').get_attribute("aria-label")
        date_text = result_elem.locator('//span[@class="rsqaWe"]').inner_text()
        reviewer = result_elem.locator('div.d4r55 ').inner_text()
        try:
            reviewer_stats = result_elem.locator('div.RfnDt ').inner_text(timeout=1500)
        except PlaywrightTimeoutError:
            reviewer_stats = None
            logger.warning("no reviewer stats")
    
        extra_data = result_elem.locator('div.PBK6be').all_inner_texts()
        print(reviewer, reviewer_stats, extra_data)
        date = dateparser.parse(date_text)
        slight_delay()
        item = RestaurantReview(id=review_idx + 1, text=text, stars=self.clean_stars(stars), date=str(date))
        print(item)
        return item

   
    
    def clean_stars(self,stars_text):
        return stars_text.split(" stars")[0]
    
    def close(self):
        self.browser.close()