from tortoise import Tortoise, run_async
from loguru import logger
import os
from benz_scraper.models import Restaurant
from tortoise.exceptions import IntegrityError

from dotenv import load_dotenv

load_dotenv()
DATABASE_URI = os.environ.get("DATABASE_URI")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URI},
    "apps": {
        "models": {
            "models": ["benz_scraper.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url=DATABASE_URI,
        modules={'models': ['benz_scraper.models']},
        
    )
    # Generate the schema
    await Tortoise.generate_schemas()
    
    
# run_async(init())

from tortoise.transactions import atomic

@atomic()
async def create_restaurant(name, href, pricing, av_stars, category, url, address, description, cover_img):
    try:
        r = await Restaurant.create(name=name, href=href, pricing=pricing,av_stars=av_stars,
            category = category,
            url=url,
            address= address,
            description =  description,
            cover_img = cover_img)
        logger.info(f"restaurent {name} is created" )
        return r
    except IntegrityError as e:
        logger.warning(f"item exists {e}")
        # raise e
# async def clean():
    
#     from tortoise import connections
    

#     TORTOISE_ORM = {
#         "connections": {"default": "postgres://soubenz:S30hOB44yloc8QY@173.249.24.218:5433/sentimatics"},
#         "apps": {
#             "models": {
#                 "models": ["benz_scraper.models", "aerich.models"],
#                 "default_connection": "default",
#             },
#         },
#     }
#     await Tortoise.init(
#         db_url="postgres://soubenz:S30hOB44yloc8QY@173.249.24.218:5432/sentimatics",
#         modules={'models': ['benz_scraper.models']},
        
#     )
#     conn = connections.get("default")
#     await conn.close_all()
    
    
# run_async(clean())