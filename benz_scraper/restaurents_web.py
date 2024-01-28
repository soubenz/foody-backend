from math import floor
import re
from playwright.sync_api import sync_playwright
import time
from pydantic import BaseModel
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from loguru import logger
from playwright_stealth import stealth_sync
from benz_scraper.scrapers.reviews_scraper import ReviewsScraper
from benz_scraper.utils import debug_delay, dump_items_to_json, parse_date, slight_delay
from datetime import datetime, timedelta
import dateparser



class Scrape_Google:
    
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
        #  "https://www.google.com/maps/place/Nabou+Pastel+Paris+19%C3%A8me/@48.8942894,2.3783428,17z/data=!4m6!3m5!1s0x47e66d3c5de986f9:0xac4b79771d885c92!8m2!3d48.8939687!4d2.3814685!16s%2Fg%2F11h88czw4_?hl=en&entry=ttu"
        self.page.goto(url)
        slight_delay()
        logger.info("Page is loaded")
        
    def prepare_reviews(self):
             
        button = self.page.locator('//button[@data-tab-index="1"]').click()
        time.sleep(2)
        button = self.page.locator('//button[@data-value="Sort"]').click()
        time.sleep(2)
        menu = self.page.locator('div#action-menu')

        menu.locator('//div[@role="menuitemradio"][@data-index="1"]').click()
        self.reviews = self.page.locator('div.jftiEf')
        
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
        
        
    def scrape_review(self, review_idx):
        result_elem = self.reviews.nth(review_idx)
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

def scrape_restaurants():
    with sync_playwright() as playwright:
        b = ReviewsScraper(playwright)
        b.navigate("https://www.google.com/maps/place/Nabou+Pastel+Paris+19%C3%A8me/@48.8942894,2.3783428,17z/data=!4m6!3m5!1s0x47e66d3c5de986f9:0xac4b79771d885c92!8m2!3d48.8939687!4d2.3814685!16s%2Fg%2F11h88czw4_?hl=en&entry=ttu")
        
        b.consent_cookies()   
        b.get_metadata()
        b.prepare_reviews()
        # debug_delay()
        items = []
        print(b.true_nb)
        scrapped_item = 1
        while scrapped_item < b.true_nb:
            time.sleep(3)
            b.page.mouse.wheel(0, 100000)
            for _ in range(10):
                item = b.scrape_review(scrapped_item)
                print(item)
                items.append(item)
                # result_elem = reviews.nth(scrapped_item)
                # try:
                #     text = result_elem.locator('//div[@class="MyEned"]/span[@class="wiI7pd"]').inner_text(timeout=1500)
                # except PlaywrightTimeoutError:
                #     text= None
                # print(result_elem, text)
                # stars = result_elem.locator('//span[@class="kvMYJc"]').get_attribute("aria-label")
                # date = result_elem.locator('//span[@class="rsqaWe"]').inner_text()
                # item = RestaurantReview(id=scrapped_item + 1, text=text, stars=stars, date=date)

                scrapped_item+= 1
                
        dump_items_to_json(items, "nabou")
        
scrape_restaurants()
