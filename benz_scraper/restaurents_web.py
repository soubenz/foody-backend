from math import floor
import re
from playwright.sync_api import sync_playwright
import time
from pydantic import BaseModel
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from loguru import logger


def debug_delay():
    time.sleep(1000)


class RestaurantReview(BaseModel):
    id: int
    text: str = None
    stars: str
    date: str

class Scrape_Google:
    
    def __init__(self, playwright):
        self.browser = playwright.chromium.launch(headless=False)
        context = self.browser.new_context()
        self.page = context.new_page()
        
    def consent_cookies(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        button = self.page.locator('//form').nth(1)
        button.click()
        time.sleep(2)


    def navigate(self, url):
        #  "https://www.google.com/maps/place/Nabou+Pastel+Paris+19%C3%A8me/@48.8942894,2.3783428,17z/data=!4m6!3m5!1s0x47e66d3c5de986f9:0xac4b79771d885c92!8m2!3d48.8939687!4d2.3814685!16s%2Fg%2F11h88czw4_?hl=en&entry=ttu"
        self.page.goto(url)
        
    def prepare_reviews(self):
             
        button = self.page.locator('//button[@data-tab-index="1"]').click()
        time.sleep(2)
        button = self.page.locator('//button[@data-value="Sort"]').click()
        time.sleep(2)
        menu = self.page.locator('div#action-menu')
        # debug_delay()
        menu.locator('//div[@role="menuitemradio"][@data-index="1"]').click()
        
    def get_metadata(self):
        
        self.reviews = self.page.locator('div.jftiEf')
        nb_reviews = self.page.locator('div.jANrlb > div.fontBodySmall').inner_text()
        self.true_nb = int(nb_reviews.split(" reviews")[0])
        # print(true_nb)
        # pages = floor(true_nb / 10)
        
        
    def scrape_review(self, review_idx):
        result_elem = self.reviews.nth(review_idx)
        try:
            text = result_elem.locator('//div[@class="MyEned"]/span[@class="wiI7pd"]').inner_text(timeout=1500)
        except PlaywrightTimeoutError:
            text= None
        stars = result_elem.locator('//span[@class="kvMYJc"]').get_attribute("aria-label")
        date = result_elem.locator('//span[@class="rsqaWe"]').inner_text()
        item = RestaurantReview(id=review_idx + 1, text=text, stars=stars, date=date)
        print(item)
        return item
    
    def close(self):
        self.browser.close()
    
def scrape_restaurants():
    with sync_playwright() as playwright:
        b = Scrape_Google(playwright)
        b.navigate("https://www.google.com/maps/place/Nabou+Pastel+Paris+19%C3%A8me/@48.8942894,2.3783428,17z/data=!4m6!3m5!1s0x47e66d3c5de986f9:0xac4b79771d885c92!8m2!3d48.8939687!4d2.3814685!16s%2Fg%2F11h88czw4_?hl=en&entry=ttu")
        
        # page.set_viewport_size(width=375, height=812)

        # button = page.query_selector("form:nth-child(1) > div > div > button")
        # button.click()
        # time.sleep(70)
        b.consent_cookies()

        
        b.prepare_reviews()
        b.get_metadata()
        
        print(b.true_nb)
        scrapped_item = 1
        while scrapped_item < b.true_nb:
            time.sleep(3)
            b.page.mouse.wheel(0, 100000)
            for _ in range(10):
                item = b.scrape_review(scrapped_item)
                print(item)
                # result_elem = reviews.nth(scrapped_item)
                # try:
                #     text = result_elem.locator('//div[@class="MyEned"]/span[@class="wiI7pd"]').inner_text(timeout=1500)
                # except PlaywrightTimeoutError:
                #     text= None
                # print(result_elem, text)
                # stars = result_elem.locator('//span[@class="kvMYJc"]').get_attribute("aria-label")
                # date = result_elem.locator('//span[@class="rsqaWe"]').inner_text()
                # item = RestaurantReview(id=scrapped_item + 1, text=text, stars=stars, date=date)
                # print(item)
                scrapped_item+= 1
        
        
        # time.sleep(170)
        # reviews = page.locator('//*[@id="app"]/div[12]/div[2]/div/div[2]/div[3]/div/div[3]/div/div[3]/span').inner_text()
        # return
        # data = []
        # for k in reviews:
        # page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        
        # for i in range(1):
        #     page.mouse.wheel(0, 100000)
        #     time.sleep(2)
        #     #app > div.ml-pane-container > div.visible > div > div.nkePVe > div:nth-child(3) > div:nth-child(9) > div.HQtAOc > div > div.QGH3wd.Inlyae > div > span
            
        # #     data.append(k.text_content())page.on("request", lambda request: print(">>", request.method, request.url))
        #     is_data = False
        #     # with page.expect_response(re.compile(r"lh3.googleusercontent.+")) as response_info:
        #     #     is_data = True
        #     # print(is_data)
            
        #     # page.on("response", lambda response: print("<<", response.status, response.url))
        

scrape_restaurants()
