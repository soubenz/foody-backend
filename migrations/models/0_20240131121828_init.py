from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "restuarants" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "pricing" VARCHAR(255) NOT NULL,
    "href" VARCHAR(255) NOT NULL,
    "av_stars" DECIMAL(2,1),
    "category" VARCHAR(255) NOT NULL,
    "url" VARCHAR(255) NOT NULL,
    "address" VARCHAR(255) NOT NULL UNIQUE,
    "description" TEXT,
    "cover_img" VARCHAR(500),
    "added_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "uid_restuarants_name_dbce97" UNIQUE ("name", "address")
);
CREATE INDEX IF NOT EXISTS "idx_restuarants_name_dbce97" ON "restuarants" ("name", "address");
CREATE TABLE IF NOT EXISTS "reviews" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" VARCHAR(255) NOT NULL,
    "stars" DOUBLE PRECISION NOT NULL,
    "reviewer" VARCHAR(255) NOT NULL,
    "added_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "restaurant_id" INT NOT NULL REFERENCES "restuarants" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
