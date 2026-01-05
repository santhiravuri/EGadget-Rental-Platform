import os
import ssl
import smtplib
from email.message import EmailMessage
from typing import Tuple, Optional
import traceback
def _mail_ext():
    try:
        from flask import current_app
        mail = current_app.extensions.get("mail")
        return current_app, mail
    except Exception:
        return None, None

def _smtp_client():
    host = os.getenv("SMTP_HOST") or os.getenv("SMTP_SERVER", "")
    port = int(os.getenv("SMTP_PORT", os.getenv("SMTP_PORT", "0")) or "0")
    user = os.getenv("SMTP_USERNAME") or os.getenv("SMTP_EMAIL", "")
    password = os.getenv("SMTP_PASSWORD") or os.getenv("SMTP_APP_PASSWORD", "")
    use_tls = (os.getenv("SMTP_USE_TLS", "").lower() in ("1", "true", "yes")) or (os.getenv("MAIL_USE_TLS", "true").lower() in ("1", "true", "yes"))
    return host, port, user, password, use_tls

def send_email_html(subject: str, to_address: str, html_body: str, cc=None, bcc=None):
    if not subject or not to_address or not html_body:
        return False
    app, mail = _mail_ext()
    if mail and app:
        try:
            from flask_mail import Message
            sender = app.config.get("MAIL_DEFAULT_SENDER") or os.getenv("SMTP_EMAIL")
            msg = Message(subject, recipients=[to_address], html=html_body, sender=sender)
            mail.send(msg)
            print(f"EMAIL OK: {subject} -> {to_address}")
            return True
        except Exception as e:
            debug = os.getenv("SMTP_DEBUG", os.getenv("EMAIL_DEBUG", "false")).lower() in ("1", "true", "yes")
            print(f"EMAIL FAIL: {subject} -> {to_address} err={e}")
            if debug:
                try:
                    if hasattr(e, "smtp_code"):
                        print(f"SMTP CODE: {getattr(e, 'smtp_code', None)}")
                    if hasattr(e, "smtp_error"):
                        print(f"SMTP ERROR: {getattr(e, 'smtp_error', None)}")
                except Exception:
                    pass
                try:
                    traceback.print_exc()
                except Exception:
                    pass
            # fall through to SMTP fallback
    frm = os.getenv("SMTP_FROM", os.getenv("FROM_EMAIL", os.getenv("SMTP_EMAIL", "no-reply@egadget-rent.local")))
    host, port, user, password, use_tls = _smtp_client()
    debug = os.getenv("SMTP_DEBUG", os.getenv("EMAIL_DEBUG", "false")).lower() in ("1", "true", "yes")
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = frm
    msg["To"] = to_address
    if cc:
        msg["Cc"] = cc
    if bcc:
        msg["Bcc"] = bcc
    msg.set_content("This is an HTML email. Please view it in an HTML-capable client.")
    msg.add_alternative(html_body, subtype="html")
    try:
        if use_tls:
            context = ssl.create_default_context()
            with smtplib.SMTP(host, port) as server:
                if debug:
                    server.set_debuglevel(1)
                server.starttls(context=context)
                if user and password:
                    server.login(user, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, port) as server:
                if debug:
                    server.set_debuglevel(1)
                if user and password:
                    server.login(user, password)
                server.send_message(msg)
        print(f"EMAIL OK: {subject} -> {to_address}")
        return True
    except Exception as e:
        print(f"EMAIL FAIL: {subject} -> {to_address} err={e}")
        if debug:
            try:
                if hasattr(e, "smtp_code"):
                    print(f"SMTP CODE: {getattr(e, 'smtp_code', None)}")
                if hasattr(e, "smtp_error"):
                    print(f"SMTP ERROR: {getattr(e, 'smtp_error', None)}")
            except Exception:
                pass
            try:
                traceback.print_exc()
            except Exception:
                pass
        return False

def _render_in_app(app, template_name: str, **ctx) -> str:
    try:
        with app.app_context():
            from flask import render_template
            return render_template(template_name, **ctx)
    except Exception as e:
        print(f"EMAIL RENDER FAIL: template={template_name} err={e}")
        return ""

def send_order_confirmation_email(app, order: dict, user: dict) -> bool:
    to = (user or {}).get("email")
    if not to:
        return False
    html = _render_in_app(app, "email/order_confirmation.html", order=order, user=user)
    return send_email_html("Order Confirmed – eGadget Rent", to, html) if html else False

# Admin notifications removed per user-only recipient policy.

def send_order_cancellation_email(app, order: dict, reason: str, cancelled_at: str, refund_timeline: str | None) -> bool:
    user_id = order.get("user_id")
    to = None
    try:
        from bson import ObjectId
        from models.db import users_col
        user = users_col.find_one({"_id": ObjectId(user_id)})
        to = (user or {}).get("email")
    except Exception:
        pass
    if not to:
        return False
    html = _render_in_app(app, "email/order_cancellation.html", order=order, reason=reason, cancelled_at=cancelled_at, refund_timeline=refund_timeline)
    return send_email_html("Order Cancelled – eGadget Rent", to, html) if html else False

def send_return_reminder_email(app, order: dict, user: dict, return_date_str: str) -> bool:
    to = (user or {}).get("email")
    if not to:
        return False
    html = _render_in_app(app, "email/return_reminder.html", order=order, user=user, return_date_str=return_date_str)
    return send_email_html("Reminder: Rental Return Due Tomorrow", to, html) if html else False

def send_late_penalty_email(app, order: dict, user: dict, original_return_date_str: str, days_late: int, penalty_per_day: float, total_penalty: float) -> bool:
    to = (user or {}).get("email")
    if not to:
        return False
    html = _render_in_app(app, "email/late_penalty.html", order=order, user=user, original_return_date_str=original_return_date_str, days_late=days_late, penalty_per_day=penalty_per_day, total_penalty=total_penalty)
    return send_email_html("Late Return Penalty Applied", to, html) if html else False
