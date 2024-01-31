from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "restuarants" DROP COLUMN "href";
        ALTER TABLE "restuarants" ALTER COLUMN "address" TYPE VARCHAR(500) USING "address"::VARCHAR(500);
        ALTER TABLE "restuarants" ALTER COLUMN "url" TYPE VARCHAR(500) USING "url"::VARCHAR(500);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "restuarants" ADD "href" VARCHAR(255) NOT NULL;
        ALTER TABLE "restuarants" ALTER COLUMN "address" TYPE VARCHAR(255) USING "address"::VARCHAR(255);
        ALTER TABLE "restuarants" ALTER COLUMN "url" TYPE VARCHAR(255) USING "url"::VARCHAR(255);"""
