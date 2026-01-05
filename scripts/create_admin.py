import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.security import generate_password_hash
from models.db import users_col

def seed_admin(email, password, name):
    if not email or not password:
        return
    email = (email or "").strip().lower()
    name = (name or "Admin").strip()
    existing = users_col.find_one({"email": email})
    if existing:
        print(f"ADMIN SEED: {email} already exists")
        return
    users_col.insert_one({
        "name": name,
        "email": email,
        "password": generate_password_hash(password),
        "role": "admin",
        "created_at": datetime.utcnow()
    })
    print(f"ADMIN SEED: {email} created")

def run():
    load_dotenv()
    email = os.getenv("ADMIN_SEED_EMAIL", "").strip().lower()
    password = os.getenv("ADMIN_SEED_PASSWORD", "")
    name = os.getenv("ADMIN_SEED_NAME", "Admin").strip()
    if not email or not password:
        print("ADMIN SEED: missing ADMIN_SEED_EMAIL or ADMIN_SEED_PASSWORD")
    else:
        seed_admin(email, password, name)
    seed_admin(
        os.getenv("ADMIN_SEED_1_EMAIL"),
        os.getenv("ADMIN_SEED_1_PASSWORD"),
        os.getenv("ADMIN_SEED_1_NAME")
    )
    seed_admin(
        os.getenv("ADMIN_SEED_2_EMAIL"),
        os.getenv("ADMIN_SEED_2_PASSWORD"),
        os.getenv("ADMIN_SEED_2_NAME")
    )

if __name__ == "__main__":
    run()
