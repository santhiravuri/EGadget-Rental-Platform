import os
import re
from datetime import datetime, timedelta
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
import ssl
from dotenv import load_dotenv
from services.email_service import send_email_html, send_order_confirmation_email, send_order_cancellation_email
from services import scheduler

from models.db import users_col, products_col, orders_col, otp_col, admins_col, carts_col
from flask_mail import Mail, Message


load_dotenv()
def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")
    print("SMTP USER:", os.getenv("SMTP_EMAIL"))
    app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('SMTP_EMAIL')
    app.config['MAIL_PASSWORD'] = os.getenv('SMTP_APP_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('SMTP_EMAIL')
    mail = Mail(app)
    def send_email(subject, recipients, html_body):
        try:
            msg = Message(subject, recipients=recipients, html=html_body)
            mail.send(msg)
            print(f"✅ Email sent to {recipients}")
        except Exception as e:
            print(f"❌ Email failed: {e}")

    def payment_label(method: str) -> str:
        m = (method or "").strip().upper()
        if not m:
            return "Pending"
        if m == "COD":
            return "Cash on Delivery"
        if m == "UPI":
            return "UPI (Demo)"
        if m == "DEMO":
            return "Demo Payment"
        return method
    app.jinja_env.filters["payment_label"] = payment_label
    def ui_status(status: str) -> str:
        s = (status or "").strip()
        if s in ("Paid", "Pending Payment", "Confirmed", "Placed"):
            return "Placed"
        if s in ("Cancelled",):
            return "Cancelled"
        if s in ("Completed", "Returned", "Delivered"):
            return "Delivered"
        return s or "Placed"
    app.jinja_env.filters["ui_status"] = ui_status
    try:
        if os.getenv("EMAIL_SCHEDULER_ENABLED", "false").lower() in ("1","true","yes"):
            scheduler.start(app)
    except Exception as e:
        print(f"SCHEDULER START FAIL: {e}")

    def _get_cart():
        if session.get("user_id"):
            try:
                uid = ObjectId(session["user_id"])
                cart_doc = carts_col.find_one({"user_id": uid})
                if cart_doc and "items" in cart_doc:
                    return cart_doc["items"]
            except Exception:
                pass
        return session.setdefault("cart", {})

    def _save_cart(cart):
        if session.get("user_id"):
            try:
                uid = ObjectId(session["user_id"])
                carts_col.update_one(
                    {"user_id": uid},
                    {"$set": {"items": cart, "updated_at": datetime.utcnow()}},
                    upsert=True
                )
            except Exception:
                pass
        else:
            session["cart"] = cart
            session.modified = True

    @app.context_processor
    def inject_globals():
        # For now, notification_count is 0. Can be extended to check actual notifications
        notification_count = 0
        if session.get("user_id"):
            # TODO: Add logic to count actual notifications from database
            pass
        orders_count = 0
        try:
            if session.get("user_id"):
                orders_count = orders_col.count_documents({"user_id": ObjectId(session["user_id"])})
        except Exception:
            orders_count = 0
        wishlist_count = 0
        try:
            if session.get("user_id"):
                user = users_col.find_one({"_id": ObjectId(session["user_id"])}, {"wishlist": 1})
                if user and user.get("wishlist"):
                    wishlist_count = len(user["wishlist"])
        except Exception:
            wishlist_count = 0
        
        cart_count = len(_get_cart())
        
        current_user_email = ""
        current_user_name = ""
        try:
            if session.get("user_id"):
                u = users_col.find_one({"_id": ObjectId(session["user_id"])}, {"email": 1, "fullname": 1, "name": 1})
                current_user_email = (u or {}).get("email") or ""
                current_user_name = (u or {}).get("fullname") or (u or {}).get("name") or ""
        except Exception:
            current_user_email = ""
            current_user_name = ""
        return {
            "logged_in": bool(session.get("user_id")),
            "is_admin": session.get("role") == "admin",
            "cart_count": cart_count,
            "notification_count": notification_count,
            "orders_count": orders_count,
            "wishlist_count": wishlist_count,
            "current_user_email": current_user_email,
            "current_user_name": current_user_name,
        }

    def get_current_user():
        user_id = session.get("user_id")
        if not user_id:
            return None
        return users_col.find_one({"_id": ObjectId(user_id)})
    
    def get_logged_in_user_email():
        uid = session.get("user_id")
        if not uid:
            return None
        try:
            u = users_col.find_one({"_id": ObjectId(uid)}, {"email": 1})
            return (u or {}).get("email")
        except Exception:
            return None

    @app.route("/")
    def home():
        query = request.args.get("q", "").strip()
        category = request.args.get("category", "").strip()
        filter_query = {}
        categories = products_col.distinct("category")
        if query:
            lq = query.lower()
            cat_map = {c.lower(): c for c in categories}
            mega = {
                "Mobiles": ["Smartphones", "Feature Phones", "Tablets", "Mobile Accessories", "Refurbished Mobiles"],
                "Laptops": ["Laptops", "Gaming Laptops", "Desktops", "Monitors", "Keyboards & Mouse"],
                "Cameras": ["DSLR", "Mirrorless", "Action Cameras", "Webcams", "Drones"],
                "Headphones": ["Wired Headphones", "Wireless Headphones", "Earbuds", "Bluetooth Speakers", "Sound Bars"],
                "Smart Watches": ["Smart Watches", "Fitness Bands", "Health Trackers"],
                "Gaming Consoles": ["PlayStation", "Xbox", "Handheld Console", "Controllers", "VR Headsets"],
                "Accessories": ["Chargers", "Power Banks", "Cables", "Storage Devices", "Adaptors"],
            }
            sub_set = {s.lower() for subs in mega.values() for s in subs}
            if lq in cat_map:
                filter_query = {"category": cat_map[lq]}
            elif lq in sub_set:
                rs = re.compile(rf'^{re.escape(query)}$', re.IGNORECASE)
                filter_query = {"$or": [{"subcategory": rs}, {"sub": rs}, {"meta.subcategory": rs}, {"details.subcategory": rs}]}
            else:
                filter_query = {"name": {"$regex": query, "$options": "i"}}
        elif category:
            filter_query["category"] = category
        products = list(products_col.find(filter_query).sort("name", 1))
        # Calculate average ratings for products
        for product in products:
            reviews = product.get("reviews", [])
            if reviews:
                avg = sum([float(r.get("rating", 0)) for r in reviews]) / len(reviews)
                product["avg_rating"] = round(avg, 1)
                product["reviews_count"] = len(reviews)
            else:
                product["avg_rating"] = None
                product["reviews_count"] = 0
            # expose string id for templates
            try:
                product["id"] = str(product.get("_id"))
            except Exception:
                product["id"] = None
        return render_template("index.html", products=products, categories=categories, selected_category=category, search_query=query, show_footer=True)

    @app.route('/catalog')
    def catalog():
        # Supports filtering by category and sub-category via query params
        category = request.args.get('category', '').strip()
        sub = request.args.get('sub', '').strip()
        q = request.args.get('q', '').strip()

        filter_query = {}
        if q:
            lq = q.lower()
            categories = products_col.distinct('category')
            cat_map = {c.lower(): c for c in categories}
            mega = {
                "Mobiles": ["Smartphones", "Feature Phones", "Tablets", "Mobile Accessories", "Refurbished Mobiles"],
                "Laptops": ["Laptops", "Gaming Laptops", "Desktops", "Monitors", "Keyboards & Mouse"],
                "Cameras": ["DSLR", "Mirrorless", "Action Cameras", "Webcams", "Drones"],
                "Headphones": ["Wired Headphones", "Wireless Headphones", "Earbuds", "Bluetooth Speakers", "Sound Bars"],
                "Smart Watches": ["Smart Watches", "Fitness Bands", "Health Trackers"],
                "Gaming Consoles": ["PlayStation", "Xbox", "Handheld Console", "Controllers", "VR Headsets"],
                "Accessories": ["Chargers", "Power Banks", "Cables", "Storage Devices", "Adaptors"],
            }
            sub_set = {s.lower() for subs in mega.values() for s in subs}
            if lq in cat_map:
                filter_query = {"category": cat_map[lq]}
            elif lq in sub_set:
                rs = re.compile(rf'^{re.escape(q)}$', re.IGNORECASE)
                filter_query = {"$or": [{"subcategory": rs}, {"sub": rs}, {"meta.subcategory": rs}, {"details.subcategory": rs}]}
            else:
                filter_query = {"name": {"$regex": q, "$options": "i"}}
        elif category:
            filter_query['category'] = category
        if sub:
            # Support multiple possible schema locations for subcategory (case-insensitive exact match)
            re_sub = re.compile(rf'^{re.escape(sub)}$', re.IGNORECASE)
            # Default: allow matching subcategory across several possible fields
            filter_query['$or'] = [
                {'subcategory': re_sub},
                {'sub': re_sub},
                {'tags': re_sub},
                {'meta.subcategory': re_sub},
                {'details.subcategory': re_sub},
            ]
            # Special-case: Mobiles -> Refurbished Mobiles should be strict
            if category and category.lower() == 'mobiles' and sub.lower() in ('refurbished mobiles', 'refurbished phones', 'refurbished'):
                # Replace the loose $or with an exact subcategory match and require condition == 'Refurbished'
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
                # Accept either 'Refurbished' or case-insensitive 'refurbished' stored in field 'condition'
                filter_query['condition'] = re.compile(r'^refurbished$', re.IGNORECASE)
            # Special-case: if user requests Mobiles -> Smartphones, restrict to our curated 9-item display group
            if category and category.lower() == 'mobiles' and sub.lower() == 'smartphones':
                filter_query['display_group'] = 'mobiles_smartphones_2025'
            # Special-case: if user requests Mobiles -> Feature Phones, restrict to our curated 12-item display group
            if category and category.lower() == 'mobiles' and sub.lower() == 'feature phones':
                filter_query['display_group'] = 'mobiles_feature_phones_2025'
            # Special-case: if user requests Laptops -> Gaming Laptops, restrict to our curated 12-item display group
            if category and category.lower() == 'laptops' and sub.lower() == 'gaming laptops':
                filter_query['display_group'] = 'laptops_gaming_laptops_2025'
            # Special-case: if user requests Mobiles -> Tablets, restrict to our curated 12-item display group
            if category and category.lower() == 'mobiles' and sub.lower() == 'tablets':
                filter_query['display_group'] = 'mobiles_tablets_2025'
            # Special-case: if user requests Mobiles -> Mobile Accessories, restrict to our curated display group
            if category and category.lower() == 'mobiles' and sub.lower() == 'mobile accessories':
                filter_query['display_group'] = 'mobiles_mobile_accessories_2025'
            # Special-case: if user requests Laptops -> Monitors, restrict to our curated 15-item display group
            if category and category.lower() == 'laptops' and sub.lower() == 'monitors':
                filter_query['display_group'] = 'laptops_monitors_2025'
            # Special-case: if user requests Laptops -> Desktops, restrict to our curated 15-item display group
            if category and category.lower() == 'laptops' and sub.lower() == 'desktops':
                filter_query['display_group'] = 'laptops_desktops_2025'
            # Special-case: if user requests Laptops -> Keyboards & Mouse, restrict to our curated display group
            if category and category.lower() == 'laptops' and sub.lower() == 'keyboards & mouse':
                filter_query['display_group'] = 'laptops_keyboards_mouse_2025'
            # Special-case: Cameras -> DSLR should be strict (exact subcategory)
            if category and category.lower() == 'cameras' and sub.lower() == 'dslr':
                # require exact subcategory match and avoid loose matching across tags
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
            # Special-case: Cameras -> Mirrorless should be strict (exact subcategory)
            if category and category.lower() == 'cameras' and sub.lower() == 'mirrorless':
                # require exact subcategory match and avoid loose matching across tags
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
            # Special-case: Cameras -> Action Cameras should be strict (exact subcategory)
            if category and category.lower() == 'cameras' and sub.lower() in ('action cameras', 'action'):
                # require exact subcategory match and avoid loose matching across tags
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
            # Special-case: Cameras -> Webcams should be strict (exact subcategory)
            if category and category.lower() == 'cameras' and sub.lower() in ('webcams', 'webcam'):
                # require exact subcategory match and avoid loose matching across tags
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
            # Special-case: Cameras -> Drones should be strict (exact subcategory)
            if category and category.lower() == 'cameras' and sub.lower() in ('drones', 'drone'):
                # require exact subcategory match and avoid loose matching across tags
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub

            # Special-case: Headphones -> Wireless Headphones should be strict
            if category and category.lower() == 'headphones' and sub.lower() == 'wireless headphones':
                # require exact subcategory match
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
            
            # Special-case: Headphones -> Earbuds should be strict
            if category and category.lower() == 'headphones' and sub.lower() == 'earbuds':
                # require exact subcategory match
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
            
            # Special-case: Headphones -> Wired Headphones should be strict
            if category and category.lower() == 'headphones' and sub.lower() == 'wired headphones':
                # require exact subcategory match
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub

            # Special-case: Headphones -> Bluetooth Speakers should be strict
            if category and category.lower() == 'headphones' and sub.lower() == 'bluetooth speakers':
                # require exact subcategory match
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub

            # Special-case: Headphones -> Sound Bars should be strict
            if category and category.lower() == 'headphones' and sub.lower() == 'sound bars':
                # require exact subcategory match
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
            if category and category.lower() == 'smart watches' and sub.lower() in ('smart watches', 'fitness bands', 'health trackers'):
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
            if category and category.lower() == 'accessories' and sub.lower() in ('chargers', 'power banks', 'cables'):
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
            if category and category.lower() == 'accessories' and sub.lower() in ('storage devices', 'adaptors'):
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
            if category and category.lower() == 'gaming consoles' and sub.lower() in ('playstation', 'xbox', 'handheld console', 'controllers'):
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
            if category and category.lower() in ('gaming console', 'gaming consoles') and sub.lower() == 'vr headsets':
                filter_query.pop('$or', None)
                filter_query['subcategory'] = re_sub
                filter_query['category'] = re.compile(r'^gaming console(s)?$', re.IGNORECASE)
        
        # Special-case: if user requests Laptops category, restrict to our curated 14-item display group
        if category and category.lower() == 'laptops' and not sub:
            filter_query['display_group'] = 'laptops_2025'

        categories = products_col.distinct('category')
        products = list(products_col.find(filter_query).sort('name', 1))
        # Prepare ratings
        for product in products:
            reviews = product.get('reviews', [])
            if reviews:
                avg = sum([float(r.get('rating', 0)) for r in reviews]) / len(reviews)
                product['avg_rating'] = round(avg, 1)
                product['reviews_count'] = len(reviews)
            else:
                product['avg_rating'] = None
                product['reviews_count'] = 0
            # expose string id for templates
            try:
                product['id'] = str(product.get('_id'))
            except Exception:
                product['id'] = None

        return render_template('catalog.html', products=products, categories=categories, selected_category=category, selected_sub=sub, search_query=q)

    @app.route("/search")
    def search():
        q = request.args.get('q', '').strip()
        category = ''
        sub = ''
        filter_query = {}
        if q:
            lq = q.lower()
            categories = products_col.distinct('category')
            cat_map = {c.lower(): c for c in categories}
            mega = {
                "Mobiles": ["Smartphones", "Feature Phones", "Tablets", "Mobile Accessories", "Refurbished Mobiles"],
                "Laptops": ["Laptops", "Gaming Laptops", "Desktops", "Monitors", "Keyboards & Mouse"],
                "Cameras": ["DSLR", "Mirrorless", "Action Cameras", "Webcams", "Drones"],
                "Headphones": ["Wired Headphones", "Wireless Headphones", "Earbuds", "Bluetooth Speakers", "Sound Bars"],
                "Smart Watches": ["Smart Watches", "Fitness Bands", "Health Trackers"],
                "Gaming Consoles": ["PlayStation", "Xbox", "Handheld Console", "Controllers", "VR Headsets"],
                "Accessories": ["Chargers", "Power Banks", "Cables", "Storage Devices", "Adaptors"],
            }
            sub_set = {s.lower() for subs in mega.values() for s in subs}
            if lq in cat_map:
                category = cat_map[lq]
                filter_query = {"category": category}
            elif lq in sub_set:
                rs = re.compile(rf'^{re.escape(q)}$', re.IGNORECASE)
                filter_query = {"$or": [{"subcategory": rs}, {"sub": rs}, {"meta.subcategory": rs}, {"details.subcategory": rs}]}
                sub = q
            else:
                filter_query = {
                    "$or": [
                        {"name": {"$regex": q, "$options": "i"}},
                        {"brand_name": {"$regex": q, "$options": "i"}},
                        {"model_name": {"$regex": q, "$options": "i"}},
                        {"brand": {"$regex": q, "$options": "i"}}
                    ]
                }
        products = list(products_col.find(filter_query).sort('name', 1))
        for product in products:
            reviews = product.get('reviews', [])
            if reviews:
                avg = sum([float(r.get('rating', 0)) for r in reviews]) / len(reviews)
                product['avg_rating'] = round(avg, 1)
                product['reviews_count'] = len(reviews)
            else:
                product['avg_rating'] = None
                product['reviews_count'] = 0
            try:
                product['id'] = str(product.get('_id'))
            except Exception:
                product['id'] = None
        categories = products_col.distinct('category')
        return render_template('catalog.html', products=products, categories=categories, selected_category=category, selected_sub=sub, search_query=q)
    @app.route("/product/<product_id>")
    def product_detail(product_id: str):
        oid = safe_oid(product_id)
        if not oid:
            flash("Product not found", "danger")
            return redirect(url_for("home"))
        product = products_col.find_one({"_id": oid})
        if not product:
            flash("Product not found", "danger")
            return redirect(url_for("home"))
        reviews = product.get("reviews", [])
        if reviews:
            avg = sum([float(r.get("rating", 0)) for r in reviews]) / max(len(reviews), 1)
            product["avg_rating"] = round(avg, 1)
            product["reviews_count"] = len(reviews)
        else:
            product["avg_rating"] = None
            product["reviews_count"] = 0
        # expose string id for templates and ensure simple availability of subcategory
        try:
            product['id'] = str(product.get('_id'))
        except Exception:
            product['id'] = None
        # normalize subcategory fields
        if not product.get('subcategory') and product.get('sub'):
            product['subcategory'] = product.get('sub')
        # fetch related products from same category (exclude current)
        related = list(products_col.find({"category": product.get('category', ''), "_id": {"$ne": product.get('_id')}}).limit(4))
        for r in related:
            try:
                r['id'] = str(r.get('_id'))
            except Exception:
                r['id'] = None
        return render_template("product_detail.html", product=product, related_products=related)

    @app.post("/api/rental/start")
    def api_rental_start():
        pid = request.form.get("product_id")
        days = int(request.form.get("days", 1))
        qty = int(request.form.get("quantity", 1))
        delivery_date = request.form.get("delivery_date", "").strip()
        location = request.form.get("location", "").strip()
        total = float(request.form.get("total", 0))
        deposit = float(request.form.get("deposit", 0))
        if days <= 0 or qty <= 0 or not delivery_date:
            return jsonify({"ok": False, "message": "Invalid rental parameters"}), 400
        if not location:
            return jsonify({"ok": False, "message": "Location is required to place an order"}), 400
        oid = safe_oid(pid)
        if not oid:
            return jsonify({"ok": False, "message": "Invalid product ID"}), 400
        product = products_col.find_one({"_id": oid})
        if not product:
            return jsonify({"ok": False, "message": "Product not found"}), 404
        session["pending_rental"] = {
            "product_id": pid,
            "days": days,
            "quantity": qty,
            "delivery_date": delivery_date,
            "location": location,
            "rent_per_day": float(product.get("rent_per_day", 0)),
            "total": total,
            "deposit": deposit,
            "name": product.get("name"),
            "brand": product.get("brand"),
            "brand_name": product.get("brand_name") or product.get("brand"),
            "model_name": product.get("model_name") or product.get("name"),
            "image_url": product.get("image_url"),
            "category": product.get("category"),
            "subcategory": product.get("subcategory") or product.get("sub"),
        }
        redirect_url = url_for("login") if not session.get("user_id") else url_for("order_summary")
        return jsonify({"ok": True, "redirect_url": redirect_url})

    @app.route("/order-summary")
    def order_summary():
        pr = session.get("pending_rental")
        if not pr:
            flash("No rental in progress", "warning")
            return redirect(url_for("home"))
        return render_template("order_summary.html", rental=pr)

    @app.get("/api/search/suggest")
    def api_search_suggest():
        q = request.args.get("q", "").strip()
        if not q:
            return jsonify({"ok": True, "suggestions": []})
        regex = re.compile(re.escape(q), re.IGNORECASE)
        suggestions = []
        # Product name suggestions
        products = list(products_col.find({
            "$or": [
                {"name": {"$regex": regex}},
                {"brand_name": {"$regex": regex}},
                {"model_name": {"$regex": regex}},
                {"brand": {"$regex": regex}},
            ]
        }).limit(8))
        for p in products:
            pid = str(p.get("_id"))
            label = f"{p.get('brand_name') or p.get('brand') or ''} {p.get('model_name') or p.get('name') or ''}".strip()
            suggestions.append({
                "type": "product",
                "label": label,
                "meta": {
                    "category": p.get("category"),
                    "subcategory": p.get("subcategory") or p.get("sub"),
                    "price": p.get("rent_per_day"),
                },
                "url": url_for("product_detail", product_id=pid),
            })
        # Subcategory suggestions based on curated mapping
        MEGA_DATA = {
            "Mobiles": ["Smartphones", "Feature Phones", "Tablets", "Mobile Accessories", "Refurbished Mobiles"],
            "Laptops": ["Laptops", "Gaming Laptops", "Desktops", "Monitors", "Keyboards & Mouse"],
            "Cameras": ["DSLR", "Mirrorless", "Action Cameras", "Webcams", "Drones"],
            "Headphones": ["Wired Headphones", "Wireless Headphones", "Earbuds", "Bluetooth Speakers", "Sound Bars"],
            "Smart Watches": ["Smart Watches", "Fitness Bands", "Health Trackers"],
            "Gaming Consoles": ["PlayStation", "Xbox", "Handheld Console", "Controllers", "VR Headsets"],
            "Accessories": ["Chargers", "Power Banks", "Cables", "Storage Devices", "Adaptors"],
        }
        for cat, subs in MEGA_DATA.items():
            for sub in subs:
                if regex.search(sub):
                    suggestions.append({
                        "type": "subcategory",
                        "label": f"{cat} • {sub}",
                        "url": url_for("catalog") + f"?category={cat}&sub={sub}",
                    })
        # Limit total suggestions
        suggestions = suggestions[:10]
        return jsonify({"ok": True, "suggestions": suggestions})

    # Wishlist
    @app.post("/api/wishlist/toggle")
    def api_wishlist_toggle():
        if not session.get("user_id"):
            return jsonify({"ok": False, "success": False, "message": "Login required"}), 401
        
        product_id = request.form.get("product_id")
        oid = safe_oid(product_id)
        if not oid:
            return jsonify({"ok": False, "success": False, "message": "Invalid product ID"}), 400
            
        user_id = ObjectId(session["user_id"])
        user = users_col.find_one({"_id": user_id}, {"wishlist": 1}) or {}
        
        # Ensure consistent string IDs
        wishlist = set([str(x) for x in user.get("wishlist", []) if safe_oid(x)])
        pid_str = str(oid)
        
        state = None
        if pid_str in wishlist:
            wishlist.remove(pid_str)
            state = "removed"
        else:
            wishlist.add(pid_str)
            state = "added"
            
        users_col.update_one({"_id": user_id}, {"$set": {"wishlist": [ObjectId(x) for x in wishlist]}})
        return jsonify({"ok": True, "success": True, "state": state, "in_wishlist": state == "added", "wishlist_count": len(wishlist)})

    @app.post("/api/wishlist/remove")
    def api_wishlist_remove():
        if not session.get("user_id"):
            return jsonify({"ok": False, "success": False, "message": "Login required"}), 401
            
        product_id = request.form.get("product_id")
        oid = safe_oid(product_id)
        if not oid:
            return jsonify({"ok": False, "success": False, "message": "Invalid product ID"}), 400
            
        user_id = ObjectId(session["user_id"])
        # Use $pull for atomic removal
        users_col.update_one({"_id": user_id}, {"$pull": {"wishlist": oid}})
        
        # Get updated count
        user = users_col.find_one({"_id": user_id}, {"wishlist": 1})
        wishlist_count = len(user.get("wishlist", [])) if user else 0
        
        return jsonify({"ok": True, "success": True, "wishlist_count": wishlist_count})

    @app.post("/api/wishlist/to-cart")
    def api_wishlist_to_cart():
        if not session.get("user_id"):
            return jsonify({"ok": False, "success": False, "message": "Login required"}), 401
            
        product_id = request.form.get("product_id")
        oid = safe_oid(product_id)
        if not oid:
            return jsonify({"ok": False, "success": False, "message": "Invalid product ID"}), 400
            
        # Add to cart
        cart = _get_cart()
        pid_str = str(oid)
        
        if pid_str in cart:
            cart[pid_str]["quantity"] = cart[pid_str].get("quantity", 1) + 1
        else:
            cart[pid_str] = {"days": 1, "quantity": 1}
        _save_cart(cart)
        
        # Remove from wishlist (sync)
        user_id = ObjectId(session["user_id"])
        users_col.update_one({"_id": user_id}, {"$pull": {"wishlist": oid}})
        
        # Get updated wishlist count
        user = users_col.find_one({"_id": user_id}, {"wishlist": 1})
        wishlist_count = len(user.get("wishlist", [])) if user else 0
        
        return jsonify({
            "ok": True, 
            "success": True,
            "cart_count": len(cart), 
            "wishlist_count": wishlist_count,
            "message": "Moved to cart"
        })

    @app.route("/wishlist")
    def wishlist_page():
        if not session.get("user_id"):
            flash("Please login to view wishlist", "warning")
            return redirect(url_for("login"))
        user = get_current_user()
        ids = [pid for pid in (user or {}).get("wishlist", [])]
        products = list(products_col.find({"_id": {"$in": ids}})) if ids else []
        for p in products:
            try:
                p["id"] = str(p.get("_id"))
            except Exception:
                p["id"] = None
        return render_template("wishlist.html", products=products)

    # Reviews & Ratings
    @app.post("/product/<product_id>/review")
    def add_review(product_id: str):
        if not session.get("user_id"):
            flash("Please login to review", "warning")
            return redirect(url_for("login"))
        rating = int(request.form.get("rating", 0))
        comment = request.form.get("comment", "").strip()
        rating = min(5, max(1, rating))
        review = {
            "user_id": ObjectId(session["user_id"]),
            "name": session.get("name"),
            "rating": rating,
            "comment": comment,
            "created_at": datetime.utcnow(),
            "review_id": str(ObjectId()),  # Unique ID for deletion
        }
        products_col.update_one({"_id": ObjectId(product_id)}, {"$push": {"reviews": review}})
        flash("Thanks for your review!", "success")
        return redirect(url_for("product_detail", product_id=product_id))

    # Auth
    @app.post("/api/auth/send-otp")
    def api_send_otp():
        email = request.form.get("email", "").strip().lower()
        if not email:
            return jsonify({"ok": False, "message": "Email is required"}), 400
        
        # Check if email already registered
        if users_col.find_one({"email": email}):
             return jsonify({"ok": False, "message": "Email already registered"}), 400

        # Prevent Spam: Check if OTP sent in last 60 seconds
        last_otp = otp_col.find_one({
            "destination": email,
            "type": "registration",
            "created_at": {"$gt": datetime.utcnow() - timedelta(seconds=60)}
        })
        if last_otp:
            return jsonify({"ok": False, "message": "Please wait 60s before resending OTP"}), 429

        import random
        otp_val = f"{random.randint(100000, 999999)}"
        otp_hash = generate_password_hash(otp_val)
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        
        otp_doc = {
            "destination": email,
            "otp_hash": otp_hash,
            "expires_at": expires_at,
            "type": "registration",
            "created_at": datetime.utcnow()
        }
        otp_col.insert_one(otp_doc)
        
        # Send Email
        try:
            _send_email_otp(email, otp_val)
        except Exception as e:
            print(f"Error sending email: {e}")
            return jsonify({"ok": False, "message": "Failed to send email. Check server logs."}), 500
            
        return jsonify({"ok": True, "message": f"OTP sent to {email}"})

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            fullname = request.form.get("fullname", "").strip()
            email = request.form.get("email", "").strip().lower()
            mobile = request.form.get("mobile", "").strip()
            password = request.form.get("password", "")
            confirm = request.form.get("confirm_password", "")
            otp_input = request.form.get("otp", "").strip()
            role = "user"
            
            if not fullname or not email or not mobile or not password or not confirm or not otp_input:
                flash("All fields including OTP are required", "danger")
                return redirect(url_for("register"))
            
            import re as _re
            if not _re.match(r"^[6-9]\d{9}$", mobile):
                flash("Enter a valid mobile number", "danger")
                return redirect(url_for("register"))
            if password != confirm:
                flash("Passwords do not match", "danger")
                return redirect(url_for("register"))
            if users_col.find_one({"email": email}):
                flash("Email already registered", "warning")
                return redirect(url_for("login"))
                
            # Verify OTP
            otp_record = otp_col.find_one({
                "destination": email, 
                "type": "registration",
                "expires_at": {"$gt": datetime.utcnow()}
            }, sort=[("created_at", -1)])
            
            if not otp_record or not check_password_hash(otp_record["otp_hash"], otp_input):
                flash("Invalid or expired OTP", "danger")
                return redirect(url_for("register"))
            
            hashed = generate_password_hash(password)
            user_id = users_col.insert_one({
                "fullname": fullname,
                "email": email,
                "mobile": mobile,
                "password": hashed,
                "role": role,
                "created_at": datetime.utcnow(),
            }).inserted_id
            
            # Auto Login
            session["user_id"] = str(user_id)
            session["name"] = fullname
            
            flash("Registration successful. Welcome!", "success")
            return redirect(url_for("home"))
        return render_template("register.html")

    @app.route("/forgot-password", methods=["GET", "POST"])
    def forgot_password():
        if request.method == "POST":
            identity = request.form.get("identity", "").strip().lower()
            user = users_col.find_one({"$or": [{"email": identity}, {"mobile": identity}]})
            admin = admins_col.find_one({"email": identity}) if "@" in identity else None
            target = user or admin
            if not target:
                flash("No account found for provided email/mobile", "danger")
                return redirect(url_for("forgot_password"))
            import random
            otp_val = f"{random.randint(100000, 999999)}"
            otp_hash = generate_password_hash(otp_val)
            expires_at = datetime.utcnow() + timedelta(minutes=5)
            resend_available_at = datetime.utcnow() + timedelta(seconds=60)
            otp_doc = {
                "user_id": target["_id"],
                "destination": identity,
                "otp_hash": otp_hash,
                "expires_at": expires_at,
                "attempts": 0,
                "max_attempts": 3,
                "resend_available_at": resend_available_at,
            }
            res = otp_col.insert_one(otp_doc)
            session["otp_token_id"] = str(res.inserted_id)
            # Send OTP via email or SMS depending on identity
            try:
                if "@" in identity:
                    _send_email_otp(identity, otp_val)
                else:
                    _send_sms_otp(identity, otp_val)
            except Exception:
                pass
            flash("An OTP has been sent to your registered email/mobile number", "info")
            return redirect(url_for("verify_otp"))
        return render_template("forgot_password.html")

    def _send_email_otp(to_email: str, code: str) -> None:
        # Load credentials from .env
        host = os.getenv("SMTP_SERVER") or os.getenv("SMTP_HOST")
        port = int(os.getenv("SMTP_PORT", "587"))
        user = os.getenv("SMTP_EMAIL") or os.getenv("SMTP_USER")
        password = os.getenv("SMTP_APP_PASSWORD") or os.getenv("SMTP_PASS")
        
        # Ensure sender matches authenticated user for Gmail
        from_email = user 
        
        if not host or not user or not password:
            print("SMTP Credentials missing. Check .env file.")
            return

        message = f"Subject: eGadget Rent OTP\n\nYour eGadget Rent OTP is {code}. Valid for 5 minutes."
        context = ssl.create_default_context()
        
        try:
            with smtplib.SMTP(host, port) as server:
                server.starttls(context=context)
                server.login(user, password)
                server.sendmail(from_email, to_email, message)
        except Exception as e:
            print(f"SMTP Error: {e}")
            raise e

    def _send_sms_otp(to_mobile: str, code: str) -> None:
        # Placeholder for SMS provider integration (Twilio/Textlocal/Fast2SMS)
        # Use environment variables for credentials; if not present, no-op
        # Example envs: TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM
        # For security, do not log secrets; production should implement actual API calls.
        return

    @app.route("/verify-otp", methods=["GET", "POST"])
    def verify_otp():
        token_id = session.get("otp_token_id")
        if not token_id:
            return redirect(url_for("forgot_password"))
        otp_token = otp_col.find_one({"_id": ObjectId(token_id)})
        if not otp_token:
            flash("OTP session expired. Please try again.", "warning")
            return redirect(url_for("forgot_password"))
        if request.method == "POST":
            code = request.form.get("otp", "").strip()
            now = datetime.utcnow()
            if now > otp_token["expires_at"]:
                flash("OTP expired. Please request a new one.", "danger")
                return redirect(url_for("forgot_password"))
            if otp_token.get("attempts", 0) >= otp_token.get("max_attempts", 3):
                flash("Maximum OTP attempts exceeded.", "danger")
                return redirect(url_for("forgot_password"))
            ok = check_password_hash(otp_token["otp_hash"], code)
            otp_col.update_one({"_id": otp_token["_id"]}, {"$inc": {"attempts": 1}})
            if not ok:
                flash("Invalid OTP. Please try again.", "danger")
                return redirect(url_for("verify_otp"))
            session["otp_verified_for_user_id"] = str(otp_token["user_id"])
            flash("OTP verified. You may reset your password.", "success")
            return redirect(url_for("reset_password"))
        return render_template("otp_verify.html", resend_available_at=otp_token.get("resend_available_at"))

    @app.post("/resend-otp")
    def resend_otp():
        token_id = session.get("otp_token_id")
        if not token_id:
            return redirect(url_for("forgot_password"))
        otp_token = otp_col.find_one({"_id": ObjectId(token_id)})
        if not otp_token:
            flash("OTP session expired. Please try again.", "warning")
            return redirect(url_for("forgot_password"))
        now = datetime.utcnow()
        if now < otp_token.get("resend_available_at", now):
            flash("Please wait before resending OTP.", "info")
            return redirect(url_for("verify_otp"))
        import random
        otp_val = f"{random.randint(100000, 999999)}"
        otp_hash = generate_password_hash(otp_val)
        resend_available_at = datetime.utcnow() + timedelta(seconds=60)
        otp_col.update_one({"_id": otp_token["_id"]}, {"$set": {"otp_hash": otp_hash, "resend_available_at": resend_available_at, "attempts": 0, "expires_at": datetime.utcnow() + timedelta(minutes=5)}})
        flash("OTP resent. Check your email/mobile.", "success")
        return redirect(url_for("verify_otp"))

    @app.route("/reset-password", methods=["GET", "POST"])
    def reset_password():
        uid = session.get("otp_verified_for_user_id")
        if not uid:
            return redirect(url_for("forgot_password"))
        if request.method == "POST":
            pwd = request.form.get("password", "")
            confirm = request.form.get("confirm_password", "")
            if not pwd or not confirm:
                flash("All fields are required", "danger")
                return redirect(url_for("reset_password"))
            if pwd != confirm:
                flash("Passwords do not match", "danger")
                return redirect(url_for("reset_password"))
            hashed = generate_password_hash(pwd)
            # Try update in users or admins
            users_col.update_one({"_id": ObjectId(uid)}, {"$set": {"password": hashed}})
            admins_col.update_one({"_id": ObjectId(uid)}, {"$set": {"password": hashed}})
            token_id = session.pop("otp_token_id", None)
            if token_id:
                otp_col.delete_one({"_id": ObjectId(token_id)})
            session.pop("otp_verified_for_user_id", None)
            flash("Password reset successfully. Please login again.", "success")
            return redirect(url_for("login"))
        return render_template("reset_password.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            identity = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            user = users_col.find_one({"email": identity})
            if not user or not check_password_hash(user.get("password", ""), password):
                flash("Invalid credentials", "danger")
                return redirect(url_for("login"))

            # Cart Merge Logic
            guest_cart = session.get("cart", {})
            
            session["user_id"] = str(user["_id"])  # store as string for session
            session["name"] = user.get("fullname") or user.get("name")
            session["role"] = user.get("role") or "user"
            
            # Merge guest cart into user's persistent cart
            if guest_cart:
                try:
                    user_cart = _get_cart() # Fetches from DB since user_id is set
                    updated = False
                    for pid, item in guest_cart.items():
                        if pid in user_cart:
                            user_cart[pid]["quantity"] = user_cart[pid].get("quantity", 1) + item.get("quantity", 1)
                            updated = True
                        else:
                            user_cart[pid] = item
                            updated = True
                        
                        if updated:
                            _save_cart(user_cart)
                        
                        # Clear guest cart from session
                        session.pop("cart", None)
                except Exception as e:
                    print(f"Error merging cart: {e}")

            flash("Logged in successfully", "success")
            if session.get("role") == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("home"))
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logged out", "info")
        return redirect(url_for("home"))

    @app.route("/offers")
    def offers():
        return render_template("offers.html")

    @app.route("/contact")
    def contact_us():
        return render_template("contact.html")
    
    @app.route("/about")
    def about():
        return render_template("about.html")
    
    @app.route("/faq")
    def faq():
        return render_template("faq.html")
    
    @app.route('/test-mail')
    def test_mail():
        to = os.getenv('SMTP_EMAIL') or os.getenv('TEST_EMAIL') or 'test@example.com'
        try:
            msg = Message(subject="SMTP Test – eGadget", recipients=[to], html="<b>SMTP is working</b>")
            mail.send(msg)
            print(f"✅ Test email sent to {to}")
        except Exception as e:
            print(f"❌ Test email failed: {e}")
        return "Check your inbox!"
    
    @app.route('/test-email')
    def test_email():
        to = get_logged_in_user_email()
        if not to:
            return "No user logged in – cannot send test email"
        try:
            msg = Message(subject="SMTP Test – eGadget", recipients=[to], html="<b>SMTP is working</b>")
            mail.send(msg)
            print(f"✅ Test email sent to {to}")
        except Exception as e:
            print(f"❌ Test email failed: {e}")
        return "Email sent"

    @app.route("/debug-user-email")
    def debug_user_email():
        try:
            uid = session.get("user_id")
            if not uid:
                return "No user logged in"
            from bson import ObjectId
            user = users_col.find_one({"_id": ObjectId(uid)}, {"email": 1})
            email = (user or {}).get("email")
            return email or "Email not found"
        except Exception as e:
            return f"Error: {e}"

    @app.route("/account", methods=["GET", "POST"])
    def account():
        if not session.get("user_id"):
            flash("Please login to view your account", "warning")
            return redirect(url_for("login"))
        user = users_col.find_one({"_id": ObjectId(session["user_id"])})
        if not user:
            flash("User not found", "danger")
            return redirect(url_for("login"))
        if request.method == "POST":
            address = request.form.get("address", "").strip()
            phone = request.form.get("phone", "").strip()
            update = {}
            if address:
                update["address"] = address
                update["delivery_location"] = address
            if phone:
                update["mobile"] = phone
                update["contact_phone"] = phone
            if update:
                users_col.update_one({"_id": ObjectId(session["user_id"])}, {"$set": update})
                # refresh user doc
                user = users_col.find_one({"_id": ObjectId(session["user_id"])})
                flash("Account updated", "success")
            return render_template("account.html", user=user)
        # prepare safe strings for template
        try:
            user["id"] = str(user.get("_id"))
        except Exception:
            user["id"] = ""
        return render_template("account.html", user=user)

    # Cart APIs
    # _get_cart and _save_cart are defined above in create_app scope

    # Helper for safe ObjectId
    def safe_oid(oid_str):
        try:
            return ObjectId(oid_str)
        except Exception:
            return None

    @app.post("/api/cart/add")
    def api_cart_add():
        product_id = request.form.get("product_id")
        days = int(request.form.get("days", 1))
        quantity = int(request.form.get("quantity", 1))
        
        user_id = session.get("user_id")
        print(f"DEBUG: api_cart_add user_id={user_id} product_id={product_id}")

        oid = safe_oid(product_id)
        if not oid:
            print("DEBUG: Invalid product_id")
            return jsonify({"ok": False, "success": False, "message": "Invalid product ID"}), 400

        product = products_col.find_one({"_id": oid})
        if not product:
            print("DEBUG: Product not found")
            return jsonify({"ok": False, "success": False, "message": "Product not found"}), 404
            
        cart = _get_cart()
        # Use string ID for dictionary key to ensure consistency
        pid_str = str(oid)
        
        if pid_str in cart:
            # Increment quantity if already in cart
            current_qty = cart[pid_str].get("quantity", 1)
            cart[pid_str]["quantity"] = current_qty + quantity
        else:
            cart[pid_str] = {
                "days": max(1, days),
                "quantity": max(1, quantity)
            }
            
        _save_cart(cart)
        return jsonify({"ok": True, "success": True, "cart_count": len(cart), "message": "Added to cart"})

    @app.post("/api/cart/update")
    def api_cart_update():
        product_id = request.form.get("product_id")
        days = int(request.form.get("days", 1))
        quantity = int(request.form.get("quantity", 1))
        
        print(f"DEBUG: api_cart_update product_id={product_id} days={days} qty={quantity}")
        
        oid = safe_oid(product_id)
        if not oid:
            return jsonify({"ok": False, "success": False, "message": "Invalid product ID"}), 400

        cart = _get_cart()
        pid_str = str(oid)
        
        if pid_str in cart:
            if days <= 0 or quantity <= 0:
                cart.pop(pid_str, None)
            else:
                cart[pid_str]["days"] = days
                cart[pid_str]["quantity"] = quantity
        
        _save_cart(cart)
        
        # Recalculate totals for response
        item_subtotal = 0.0
        cart_count = len(cart)
        
        # We need to fetch product to calculate price
        p = products_col.find_one({"_id": oid})
        if p:
            rent = float(p.get("rent_per_day", 0))
            item_subtotal = rent * days * quantity
            
        # Calculate full total
        ids = [safe_oid(pid) for pid in cart.keys() if safe_oid(pid)]
        products = list(products_col.find({"_id": {"$in": ids}})) if ids else []
        prod_map = {str(pr["_id"]): pr for pr in products}
        
        full_total = 0.0
        for pid, data in cart.items():
            pr = prod_map.get(pid)
            if pr:
                full_total += float(pr.get("rent_per_day", 0)) * data.get("days", 1) * data.get("quantity", 1)

        return jsonify({
            "ok": True, 
            "success": True,
            "cart": cart, 
            "cart_count": cart_count,
            "subtotal": item_subtotal,
            "total": full_total
        })

    @app.post("/api/cart/remove")
    def api_cart_remove():
        product_id = request.form.get("product_id")
        print(f"DEBUG: api_cart_remove product_id={product_id}")
        
        oid = safe_oid(product_id)
        if not oid:
             return jsonify({"ok": False, "success": False, "message": "Invalid product ID"}), 400
             
        cart = _get_cart()
        cart.pop(str(oid), None)
        _save_cart(cart)
        return jsonify({"ok": True, "success": True, "cart_count": len(cart)})

    @app.route("/cart")
    def cart_page():
        cart = _get_cart()
        product_ids = [safe_oid(pid) for pid in cart.keys()]
        product_ids = [oid for oid in product_ids if oid]
        products = list(products_col.find({"_id": {"$in": product_ids}})) if product_ids else []
        for p in products:
            try:
                p["id"] = str(p.get("_id"))
            except Exception:
                p["id"] = None
        items = []
        total = 0.0
        for p in products:
            pid = str(p["_id"]) 
            data = cart.get(pid, {})
            days = data.get("days", 1)
            quantity = data.get("quantity", 1)
            subtotal = float(p.get("rent_per_day", 0)) * days * quantity
            items.append({"product": p, "days": days, "quantity": quantity, "subtotal": subtotal})
            total += subtotal
        return render_template("cart.html", items=items, total=total)

    # Orders
    @app.post("/checkout")
    def checkout():
        if not session.get("user_id"):
            flash("Please login to place order", "warning")
            return redirect(url_for("login"))
        pr = session.get("pending_rental")
        payment_method = request.form.get("payment_method", "").strip()
        upi_id = request.form.get("upi_id", "").strip()
        upi_app = request.form.get("upi_app", "").strip()
        delivery_date_form = request.form.get("delivery_date", "").strip()
        order_items = []
        total = 0.0
        if pr:
            # validations: location (mandatory), days, quantity, delivery date, payment method
            if not pr.get("location"):
                flash("Please enter delivery location to proceed", "danger")
                return redirect(url_for("order_summary"))
            if not payment_method:
                flash("Please select a payment method", "danger")
                return redirect(url_for("order_summary"))
            if payment_method.upper() == "UPI":
                import re as _re
                if not upi_id or not _re.match(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+$", upi_id):
                    flash("Enter a valid UPI ID (e.g. name@bank)", "danger")
                    return redirect(url_for("order_summary"))
            oid = safe_oid(pr["product_id"])
            if not oid:
                flash("Invalid product ID", "danger")
                return redirect(url_for("home"))
            p = products_col.find_one({"_id": oid})
            if not p:
                flash("Product not found", "danger")
                return redirect(url_for("home"))
            price = float(p.get("rent_per_day", 0))
            days = int(pr.get("days", 1))
            qty = int(pr.get("quantity", 1))
            subtotal = price * days * qty
            order_items.append({
                "product_id": p["_id"],
                "name": p.get("name"),
                "brand": p.get("brand") or p.get("brand_name"),
                "brand_name": p.get("brand_name"),
                "model_name": p.get("model_name"),
                "image_url": p.get("image_url"),
                "days": days,
                "quantity": qty,
                "rent_per_day": price,
                "subtotal": subtotal,
                "delivery_date": pr.get("delivery_date"),
                "location": pr.get("location"),
                "security_deposit": float(pr.get("deposit", 0.0)),
            })
            total += subtotal
        else:
            cart = _get_cart()
            if not cart:
                flash("Cart is empty", "warning")
                return redirect(url_for("home"))
            product_ids = [safe_oid(pid) for pid in cart.keys()]
            product_ids = [oid for oid in product_ids if oid]
            products = list(products_col.find({"_id": {"$in": product_ids}}))
            for p in products:
                pid = str(p["_id"]) 
                days = int(cart.get(pid, {}).get("days", 1))
                qty = int(cart.get(pid, {}).get("quantity", 1))
                price = float(p.get("rent_per_day", 0))
                order_items.append({
                    "product_id": p["_id"],
                    "name": p.get("name"),
                    "days": days,
                    "quantity": qty,
                    "rent_per_day": price,
                    "subtotal": price * days * qty,
                    "delivery_date": delivery_date_form or None,
                })
                total += price * days * qty
        # First order discount 20%
        is_first_order = orders_col.count_documents({"user_id": ObjectId(session["user_id"])}) == 0
        discount = round(total * 0.20, 2) if is_first_order else 0.0
        total_after = round(total - discount, 2)
        
        # Calculate return date (days from now) - use max days from order items
        max_days = max([item.get("days", 1) for item in order_items]) if order_items else 1
        return_date = datetime.utcnow() + timedelta(days=max_days)
        
        status = "Pending Payment" if payment_method.upper() == "COD" else "Paid"
        order_doc = {
            "user_id": ObjectId(session["user_id"]),
            "items": order_items,
            "total_before_discount": total,
            "discount": discount,
            "total": total_after,
            "status": status,
            "created_at": datetime.utcnow(),
            "return_date": return_date,
            "penalty_per_day": 50.0,  # ₹50 per day late penalty
            "late_penalty": 0.0,
            "late_days": 0,
            "payment_method": payment_method,
            "delivery_location": (pr.get("location") if pr else None),
            "upi_id": (upi_id if payment_method.upper() == "UPI" else None),
            "upi_app": (upi_app if payment_method.upper() == "UPI" else None),
            "email_flags": {
                "confirmation_sent": False,
                "admin_notification_sent": False
            }
        }
        res = orders_col.insert_one(order_doc)
        order_doc["_id"] = res.inserted_id
        try:
            user = users_col.find_one({"_id": ObjectId(session["user_id"])})
            to = (user or {}).get("email")
            print("DEBUG session user_id:", session.get("user_id"))
            print("DEBUG resolved email:", to)
            if to:
                ok_user = send_order_confirmation_email(app, order_doc, user)
                if ok_user:
                    orders_col.update_one({"_id": res.inserted_id}, {"$set": {"email_flags.confirmation_sent": True}})
        except Exception as e:
            print(f"EMAIL POST-ORDER FAIL: {e}")
        try:
            carts_col.delete_many({"user_id": ObjectId(session["user_id"])})
        except Exception:
            pass
        session["cart"] = {}
        session.pop("pending_rental", None)
        session["last_order_id"] = str(res.inserted_id)
        if "application/json" in (request.headers.get("Accept") or ""):
            try:
                count = orders_col.count_documents({"user_id": ObjectId(session["user_id"])})
            except Exception:
                count = None
            return jsonify({"ok": True, "order_id": str(res.inserted_id), "orders_count": count})
        return redirect(url_for("order_success"))

    @app.route("/order-success")
    def order_success():
        oid = session.get("last_order_id")
        if not oid:
            return redirect(url_for("home"))
        order = orders_col.find_one({"_id": ObjectId(oid)})
        if not order:
            return redirect(url_for("home"))
        order["order_items"] = order.get("items", [])
        return render_template("order_success.html", order=order)

    # Admin
    from functools import wraps
    def admin_required(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get("role") != "admin":
                flash("Admin access required", "danger")
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return wrapper

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        return redirect(url_for("login"))

    # Rental Actions (Orders)
    @app.post("/order/<order_id>/cancel")
    def cancel_order(order_id: str):
        if not session.get("user_id"):
            flash("Please login", "warning")
            return redirect(url_for("login"))
        oid = safe_oid(order_id)
        if not oid:
            flash("Invalid order ID", "danger")
            return redirect(url_for("user_orders"))
        reason = request.form.get("reason", "").strip() or "No reason provided"
        order = orders_col.find_one({"_id": oid, "user_id": ObjectId(session["user_id"])})
        if not order:
            flash("Order not found", "danger")
            return redirect(url_for("user_orders"))
        if order.get("status") == "Cancelled":
            flash("Order already cancelled", "warning")
            return redirect(url_for("user_orders"))
        if ui_status(order.get("status")) != "Placed":
            flash("Order cannot be cancelled at this stage", "warning")
            return redirect(url_for("user_orders"))
        update = {
            "status": "Cancelled",
            "cancel_reason": reason,
        }
        if order.get("payment_method") and str(order.get("payment_method")).upper() != "COD":
            update["refund_status"] = "Pending"
        orders_col.update_one({"_id": oid}, {"$set": update})
        try:
            user = users_col.find_one({"_id": ObjectId(session["user_id"])})
            to = (user or {}).get("email")
            flags = order.get("email_flags", {})
            print("DEBUG session user_id:", session.get("user_id"))
            print("DEBUG resolved email:", to)
            if not flags.get("cancellation_sent"):
                cancelled_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
                refund_timeline = "3-7 business days" if str(order.get("payment_method")).upper() != "COD" else None
                ok_cancel = False
                try:
                    ok_cancel = send_order_cancellation_email(app, order, reason, cancelled_at, refund_timeline)
                except Exception as _e:
                    print(f"EMAIL CANCEL FAIL: {_e}")
                if ok_cancel:
                    orders_col.update_one({"_id": oid}, {"$set": {"email_flags.cancellation_sent": True}})
        except Exception as e:
            print(f"EMAIL CANCEL FAIL: {e}")
        flash("Order cancelled", "success")
        return redirect(url_for("user_orders"))

    @app.post("/order/<order_id>/edit-delivery")
    def edit_delivery(order_id: str):
        if not session.get("user_id"):
            flash("Please login", "warning")
            return redirect(url_for("login"))
        oid = safe_oid(order_id)
        if not oid:
            flash("Invalid order ID", "danger")
            return redirect(url_for("user_orders"))
        order = orders_col.find_one({"_id": oid, "user_id": ObjectId(session["user_id"])})
        if not order:
            flash("Order not found", "danger")
            return redirect(url_for("user_orders"))
        if ui_status(order.get("status")) != "Placed":
            flash("Delivery details cannot be edited at this stage", "warning")
            return redirect(url_for("user_orders"))
        location = request.form.get("delivery_location", "").strip()
        phone = request.form.get("phone", "").strip()
        if not location and not phone:
            flash("Provide delivery location or phone", "warning")
            return redirect(url_for("user_orders"))
        update = {}
        if location:
            update["delivery_location"] = location
        if phone:
            update["contact_phone"] = phone
        if update:
            orders_col.update_one({"_id": oid}, {"$set": update})
        flash("Delivery details updated", "success")
        return redirect(url_for("user_orders"))

    @app.post("/order/<order_id>/edit")
    def edit_order(order_id: str):
        return edit_delivery(order_id)

    @app.post("/order/<order_id>/extend")
    def extend_rental(order_id: str):
        if not session.get("user_id"):
            flash("Please login", "warning")
            return redirect(url_for("login"))
        oid = safe_oid(order_id)
        if not oid:
            flash("Invalid order ID", "danger")
            return redirect(url_for("user_orders"))
        extra_days = int(request.form.get("extra_days", "0") or "0")
        if extra_days <= 0:
            flash("Enter valid extra days", "danger")
            return redirect(url_for("user_orders"))
        order = orders_col.find_one({"_id": oid, "user_id": ObjectId(session["user_id"])})
        if not order:
            flash("Order not found", "danger")
            return redirect(url_for("user_orders"))
        if order.get("status") not in ("Confirmed", "Dispatched", "In Use"):
            flash("Order cannot be extended at this stage", "warning")
            return redirect(url_for("user_orders"))
        items = order.get("items", [])
        total_before = 0.0
        for it in items:
            d = int(it.get("days", 1)) + extra_days
            it["days"] = d
            rent = float(it.get("rent_per_day", 0))
            qty = int(it.get("quantity", 1))
            it["subtotal"] = rent * d * qty
            total_before += it["subtotal"]
        discount = float(order.get("discount", 0.0))
        total_after = round(total_before - discount, 2)
        return_date = order.get("return_date")
        try:
            if return_date:
                return_date = return_date + timedelta(days=extra_days)
            else:
                return_date = datetime.utcnow() + timedelta(days=max([it.get("days", 1) for it in items]) if items else extra_days)
        except Exception:
            return_date = datetime.utcnow() + timedelta(days=max([it.get("days", 1) for it in items]) if items else extra_days)
        orders_col.update_one(
            {"_id": oid},
            {"$set": {
                "items": items,
                "total_before_discount": round(total_before, 2),
                "total": total_after,
                "return_date": return_date
            }}
        )
        flash("Rental extended", "success")
        return redirect(url_for("user_orders"))

    @app.post("/order/<order_id>/request-pickup")
    def request_pickup(order_id: str):
        if not session.get("user_id"):
            flash("Please login", "warning")
            return redirect(url_for("login"))
        oid = safe_oid(order_id)
        if not oid:
            flash("Invalid order ID", "danger")
            return redirect(url_for("user_orders"))
        pickup_date = request.form.get("pickup_date", "").strip()
        notes = request.form.get("notes", "").strip()
        order = orders_col.find_one({"_id": oid, "user_id": ObjectId(session["user_id"])})
        if not order:
            flash("Order not found", "danger")
            return redirect(url_for("user_orders"))
        if order.get("status") not in ("In Use", "Dispatched", "Confirmed"):
            flash("Pickup request is not available for this status", "warning")
            return redirect(url_for("user_orders"))
        update = {
            "status": "Return Requested",
            "pickup_date": pickup_date or None,
            "pickup_notes": notes or None
        }
        orders_col.update_one({"_id": oid}, {"$set": update})
        flash("Pickup requested", "success")
        return redirect(url_for("user_orders"))

    @app.post("/order/<order_id>/support")
    def order_support(order_id: str):
        if not session.get("user_id"):
            flash("Please login", "warning")
            return redirect(url_for("login"))
        oid = safe_oid(order_id)
        if not oid:
            flash("Invalid order ID", "danger")
            return redirect(url_for("user_orders"))
        message = request.form.get("message", "").strip()
        if not message:
            flash("Please describe your issue", "warning")
            return redirect(url_for("user_orders"))
        order = orders_col.find_one({"_id": oid, "user_id": ObjectId(session["user_id"])})
        if not order:
            flash("Order not found", "danger")
            return redirect(url_for("user_orders"))
        req = {
            "message": message,
            "created_at": datetime.utcnow()
        }
        orders_col.update_one({"_id": oid}, {"$push": {"support_requests": req}})
        flash("Support request submitted", "success")
        return redirect(url_for("user_orders"))

    @app.get("/order/<order_id>/invoice")
    def download_invoice(order_id: str):
        if not session.get("user_id"):
            flash("Please login", "warning")
            return redirect(url_for("login"))
        oid = safe_oid(order_id)
        if not oid:
            flash("Invalid order ID", "danger")
            return redirect(url_for("user_orders"))
        order = orders_col.find_one({"_id": oid, "user_id": ObjectId(session["user_id"])})
        if not order:
            flash("Order not found", "danger")
            return redirect(url_for("user_orders"))
        lines = []
        lines.append("eGadget Rent - Invoice")
        lines.append(f"Order ID: {order.get('_id')}")
        lines.append(f"Date: {order.get('created_at')}")
        lines.append(f"Status: {order.get('status')}")
        lines.append(f"Payment: {order.get('payment_method')}")
        lines.append("")
        lines.append("Items:")
        for it in order.get("items", []):
            name = it.get("name") or f"{it.get('brand_name','')} {it.get('model_name','')}".strip()
            qty = int(it.get("quantity", 1))
            days = int(it.get("days", 1))
            rent = float(it.get("rent_per_day", 0))
            subtotal = float(it.get("subtotal", 0))
            lines.append(f"- {name} x{qty}, {days} day(s) @ ₹{rent:.2f}/day = ₹{subtotal:.2f}")
        lines.append("")
        lines.append(f"Subtotal: ₹{float(order.get('total_before_discount',0)):.2f}")
        disc = float(order.get("discount",0))
        if disc > 0:
            lines.append(f"Discount: -₹{disc:.2f}")
        late = float(order.get("late_penalty",0))
        if late > 0:
            lines.append(f"Late Penalty: +₹{late:.2f}")
        total = float(order.get("total",0)) + late
        lines.append(f"Total: ₹{total:.2f}")
        content = "\n".join(lines)
        from flask import Response
        filename = f"invoice-{order_id}.txt"
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
        return Response(content, mimetype="text/plain", headers=headers)
    @app.route("/admin/logout")
    def admin_logout():
        session.pop("admin", None)
        flash("Logged out", "info")
        return redirect(url_for("admin_login"))

    @app.route("/admin")
    @admin_required
    def admin_dashboard():
        total_products = products_col.count_documents({})
        total_orders = orders_col.count_documents({})
        pending_orders = orders_col.count_documents({"status": {"$in": ["Pending Payment"]}})
        revenue = 0.0
        try:
            for o in orders_col.find({"status": {"$in": ["Paid", "Confirmed", "Dispatched", "Delivered", "Returned"]}}, {"total": 1}):
                revenue += float(o.get("total", 0.0) or 0.0)
        except Exception:
            revenue = None
        recent_orders = list(orders_col.find().sort("created_at", -1).limit(5))
        stats = {
            "total_products": total_products,
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "revenue": revenue,
        }
        return render_template("admin/dashboard.html", stats=stats, recent_orders=recent_orders)

    @app.post("/admin/send-reminders")
    @admin_required
    def admin_send_reminders():
        try:
            scheduler.run_reminders_once(app)
            flash("Return reminders executed", "success")
        except Exception as e:
            print(f"ADMIN REMINDERS FAIL: {e}")
            flash("Failed to run reminders", "danger")
        return redirect(url_for("admin_dashboard"))

    @app.post("/admin/send-penalties")
    @admin_required
    def admin_send_penalties():
        try:
            scheduler.run_penalties_once(app)
            flash("Late penalties email executed", "success")
        except Exception as e:
            print(f"ADMIN PENALTIES FAIL: {e}")
            flash("Failed to run penalties email", "danger")
        return redirect(url_for("admin_dashboard"))

    @app.route("/admin/product/new", methods=["GET", "POST"])
    @admin_required
    def admin_product_new():
        if request.method == "POST":
            data = {
                "name": request.form.get("name", "").strip(),
                "brand_name": request.form.get("brand_name", "").strip(),
                "model_name": request.form.get("model_name", "").strip(),
                "category": request.form.get("category", "").strip(),
                "rent_per_day": float(request.form.get("rent_per_day", 0)),
                "image_url": request.form.get("image_url", "").strip(),
                "available": request.form.get("available") == "on",
                "created_at": datetime.utcnow(),
            }
            products_col.insert_one(data)
            flash("Product added", "success")
            return redirect(url_for("admin_products"))
        return render_template("admin/product_form.html", product=None)

    @app.route("/admin/product/<product_id>/edit", methods=["GET", "POST"])
    @admin_required
    def admin_product_edit(product_id: str):
        product = products_col.find_one({"_id": ObjectId(product_id)})
        if not product:
            flash("Product not found", "danger")
            return redirect(url_for("admin_products"))
        if request.method == "POST":
            update = {
                "name": request.form.get("name", "").strip(),
                "brand_name": request.form.get("brand_name", "").strip(),
                "model_name": request.form.get("model_name", "").strip(),
                "category": request.form.get("category", "").strip(),
                "rent_per_day": float(request.form.get("rent_per_day", 0)),
                "image_url": request.form.get("image_url", "").strip(),
                "available": request.form.get("available") == "on",
            }
            products_col.update_one({"_id": ObjectId(product_id)}, {"$set": update})
            flash("Product updated", "success")
            return redirect(url_for("admin_products"))
        return render_template("admin/product_form.html", product=product)

    @app.post("/admin/product/<product_id>/delete")
    @admin_required
    def admin_product_delete(product_id: str):
        products_col.delete_one({"_id": ObjectId(product_id)})
        flash("Product deleted", "info")
        return redirect(url_for("admin_products"))

    @app.route("/admin/products")
    @admin_required
    def admin_products():
        products = list(products_col.find().sort("name", 1))
        for p in products:
            try:
                p["id"] = str(p.get("_id"))
            except Exception:
                p["id"] = None
        return render_template("admin/products.html", products=products)

    @app.route("/admin/orders")
    @admin_required
    def admin_orders():
        orders = list(orders_col.find().sort("created_at", -1))
        return render_template("admin/orders.html", orders=orders)

    @app.post("/admin/order/<order_id>/status")
    @admin_required
    def admin_order_update_status(order_id: str):
        oid = safe_oid(order_id)
        if not oid:
            flash("Invalid order ID", "danger")
            return redirect(url_for("admin_orders"))
        status = request.form.get("status", "").strip()
        if not status:
            flash("Select a status", "warning")
            return redirect(url_for("admin_orders"))
        orders_col.update_one({"_id": oid}, {"$set": {"status": status}})
        flash("Order status updated", "success")
        return redirect(url_for("admin_orders"))

    @app.post("/admin/review/delete")
    @admin_required
    def admin_review_delete():
        # already protected; keep admin response for API style
        product_id = request.form.get("product_id")
        review_id = request.form.get("review_id")
        if not product_id or not review_id:
            return jsonify({"ok": False, "message": "Missing parameters"}), 400
        product = products_col.find_one({"_id": ObjectId(product_id)})
        if not product:
            return jsonify({"ok": False, "message": "Product not found"}), 404
        reviews = product.get("reviews", [])
        updated_reviews = [r for r in reviews if r.get("review_id") != review_id]
        products_col.update_one({"_id": ObjectId(product_id)}, {"$set": {"reviews": updated_reviews}})
        return jsonify({"ok": True})

    @app.route("/orders")
    def user_orders():
        if not session.get("user_id"):
            flash("Please login to view orders", "warning")
            return redirect(url_for("login"))
        from datetime import timedelta
        user_id = ObjectId(session["user_id"])
        orders = list(orders_col.find({"user_id": user_id}).sort("created_at", -1))
        for order in orders:
            order["order_items"] = order.get("items", [])
            try:
                order["id"] = str(order.get("_id"))
            except Exception:
                order["id"] = ""
            # Normalize UI status
            order["ui_status"] = ui_status(order.get("status"))
            # Format dates to strings for template safety
            dt = order.get("created_at")
            try:
                order["created_at_str"] = dt.strftime("%Y-%m-%d %H:%M") if dt else None
            except Exception:
                order["created_at_str"] = str(dt) if dt else None
            rd = order.get("return_date")
            try:
                order["return_date_str"] = rd.strftime("%Y-%m-%d") if rd else None
            except Exception:
                order["return_date_str"] = str(rd) if rd else None
            # Ensure item fields are serializable/safe
            for it in order["order_items"]:
                try:
                    if it.get("product_id") is not None:
                        it["product_id"] = str(it["product_id"])
                except Exception:
                    pass
        # Calculate late penalties for each order
        for order in orders:
            if order.get("return_date") and order.get("status") != "returned":
                return_date = order["return_date"]
                if isinstance(return_date, str):
                    try:
                        from dateutil import parser
                        return_date = parser.parse(return_date)
                    except:
                        continue
                days_late = max(0, (datetime.utcnow() - return_date).days)
                penalty_per_day = order.get("penalty_per_day", 50.0)
                late_penalty = days_late * penalty_per_day
                if late_penalty > 0:
                    orders_col.update_one(
                        {"_id": order["_id"]},
                        {"$set": {"late_days": days_late, "late_penalty": round(late_penalty, 2)}}
                    )
                    order["late_days"] = days_late
                    order["late_penalty"] = round(late_penalty, 2)
        return render_template("orders.html", orders=orders)
    
    @app.route("/my-orders")
    def my_orders_alias():
        return user_orders()

    @app.post("/place-order")
    def place_order_alias():
        return checkout()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
