import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_mongo_client() -> MongoClient:
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI not set")
    return MongoClient(mongo_uri)

client = get_mongo_client()

db_name = os.getenv("MONGO_DB_NAME", "egadget_db")
db = client[db_name]

# Collections
users_col = db["users"]
products_col = db["products"]
orders_col = db["orders"]
otp_col = db["otp_tokens"]
admins_col = db["admins"]
carts_col = db["carts"]
wishlist_col = db["wishlist"] 