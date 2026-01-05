from werkzeug.security import generate_password_hash
from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["egadget_db"]
users_col = db["users"]

admins = [
    {
        "username": "Santhi",
        "email": "admin2@gmail.com",
        "password": generate_password_hash("password"),
        "role": "admin",
        "created_at": datetime.utcnow()
    },
    {
        "username": "Aruna",
        "email": "admin2@gmail.com",
        "password": generate_password_hash("password"),
        "role": "admin",
        "created_at": datetime.utcnow()
    }
]

for admin in admins:
    if not users_col.find_one({"email": admin["email"]}):
        users_col.insert_one(admin)
        print(f"Admin added: {admin['email']}")
    else:
        print(f"Admin already exists: {admin['email']}")

