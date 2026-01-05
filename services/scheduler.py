import threading
import time
from datetime import datetime, timedelta
from bson import ObjectId
from models.db import orders_col, users_col
from services.email_service import send_return_reminder_email, send_late_penalty_email

def _render(app, template, **ctx):
    with app.app_context():
        from flask import render_template
        return render_template(template, **ctx)

def _send_return_reminder(app):
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)
    q = {
        "return_date": {"$ne": None},
        "status": {"$nin": ["Cancelled", "Returned", "Completed", "Delivered"]},
    }
    orders = list(orders_col.find(q))
    for order in orders:
        rd = order.get("return_date")
        try:
            if not rd:
                continue
            if isinstance(rd, str):
                continue
            if (rd.date() - tomorrow.date()).days != -1 and (rd.date() - now.date()).days != 1:
                continue
        except Exception:
            continue
        flags = order.get("email_flags", {})
        if flags.get("return_reminder_sent"):
            continue
        uid = order.get("user_id")
        try:
            user = users_col.find_one({"_id": ObjectId(uid)})
        except Exception:
            user = None
        to = (user or {}).get("email")
        if not to:
            continue
        ok = False
        try:
            ok = send_return_reminder_email(app, order, user, rd.strftime("%Y-%m-%d"))
        except Exception:
            ok = False
        if ok:
            orders_col.update_one({"_id": order["_id"]}, {"$set": {"email_flags.return_reminder_sent": True}})

def _send_late_penalty(app):
    now = datetime.utcnow()
    q = {
        "return_date": {"$ne": None},
        "status": {"$nin": ["Cancelled", "Returned", "Completed", "Delivered"]},
    }
    orders = list(orders_col.find(q))
    for order in orders:
        rd = order.get("return_date")
        try:
            if not rd or isinstance(rd, str):
                continue
            if now <= rd:
                continue
        except Exception:
            continue
        days_late = max(0, (now - rd).days)
        penalty_per_day = float(order.get("penalty_per_day", 50.0))
        total_penalty = round(days_late * penalty_per_day, 2)
        flags = order.get("email_flags", {})
        sent_dates = flags.get("late_penalty_dates", [])
        today_str = now.strftime("%Y-%m-%d")
        if today_str in sent_dates:
            continue
        uid = order.get("user_id")
        try:
            user = users_col.find_one({"_id": ObjectId(uid)})
        except Exception:
            user = None
        to = (user or {}).get("email")
        if not to:
            continue
        ok = False
        try:
            ok = send_late_penalty_email(app, order, user, rd.strftime("%Y-%m-%d"), days_late, penalty_per_day, total_penalty)
        except Exception:
            ok = False
        if ok:
            orders_col.update_one({"_id": order["_id"]}, {"$push": {"email_flags.late_penalty_dates": today_str}})

def start(app):
    def loop():
        while True:
            try:
                _send_return_reminder(app)
            except Exception as e:
                print(f"SCHEDULER FAIL: return reminders err={e}")
            try:
                _send_late_penalty(app)
            except Exception as e:
                print(f"SCHEDULER FAIL: late penalties err={e}")
            time.sleep(3600)
    t = threading.Thread(target=loop, daemon=True)
    t.start()

def run_reminders_once(app):
    try:
        _send_return_reminder(app)
    except Exception as e:
        print(f"SCHEDULER RUN ONCE FAIL: return reminders err={e}")

def run_penalties_once(app):
    try:
        _send_late_penalty(app)
    except Exception as e:
        print(f"SCHEDULER RUN ONCE FAIL: late penalties err={e}")
