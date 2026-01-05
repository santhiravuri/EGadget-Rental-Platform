import os
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()
def get_mongo_client() -> MongoClient:
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    return MongoClient(mongo_uri)


client = get_mongo_client()
db_name = os.getenv("MONGO_DB_NAME", "rent_egadget")
db = client[db_name]


# Collections
users_col = db["users"]
products_col = db["products"]
orders_col = db["orders"]
otp_col = db["otp_tokens"]
admins_col = db["admins"]
carts_col = db["carts"]


def ensure_indexes() -> None:
    users_col.create_index("email", unique=True)
    products_col.create_index([("name", 1)])
    products_col.create_index([("category", 1)])
    orders_col.create_index([("user_id", 1), ("created_at", -1)])
    otp_col.create_index([("user_id", 1), ("expires_at", 1)])
    admins_col.create_index("email", unique=True)
    carts_col.create_index("user_id", unique=True)


ensure_indexes()


