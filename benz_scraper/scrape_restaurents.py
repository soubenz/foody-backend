
import time
from playwright.async_api import async_playwright
import asyncio

from loguru import logger
from benz_scraper.scrapers.restaurants_scraper import RestaurantsScraper

b = RestaurantsScraper("New York", "African")
asyncio.run(b.run())
