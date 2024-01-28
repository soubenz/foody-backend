
from playwright.sync_api import sync_playwright
import time

from loguru import logger

from benz_scraper.scrapers.reviews_scraper import ReviewsScraper
from benz_scraper.utils import debug_delay, dump_items_to_json



def scrape_restaurants(url):
    with sync_playwright() as playwright:
        b = ReviewsScraper(playwright, headless=True)
        b.navigate(url)
        b.consent_cookies()   
        b.get_metadata()
        b.prepare_reviews()
        # debug_delay()
        items = []
        print(b.true_nb)
        scrapped_item = 1
        try:
            while scrapped_item < b.true_nb:
                time.sleep(3)
                b.page.mouse.wheel(0, 100000)
                for _ in range(10):
                    item = b.scrape_review(scrapped_item)
                    print(item)
                    items.append(item.text)
                    scrapped_item+= 1
                    
        except Exception as e:
            print(e)
        finally:
            dump_items_to_json(items, "nabou")
            b.close()
        # dump_items_to_json(items, "nabou")
        # b.close()
        
# scrape_restaurants(url="https://www.google.com/maps/place/Nabou+Pastel+Paris+19%C3%A8me/@48.8942894,2.3783428,17z/data=!4m6!3m5!1s0x47e66d3c5de986f9:0xac4b79771d885c92!8m2!3d48.8939687!4d2.3814685!16s%2Fg%2F11h88czw4_?hl=en&entry=ttu")
scrape_restaurants(url="https://www.google.com/maps/place/Sylla/data=!4m7!3m6!1s0x89c2f7b111bac3f1:0xc476969183643b3!8m2!3d40.8003775!4d-73.9428933!16s%2Fg%2F11s_wv9y5c!19sChIJ8cO6EbH3wokRs0M2GGlpRww?authuser=0&hl=en&rclk=1")
