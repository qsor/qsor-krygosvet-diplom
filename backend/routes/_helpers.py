from functools import wraps
from flask import session, jsonify, request

from extensions import db
from models import User, AuditLog

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return db.session.get(User, uid)

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not current_user():
            return jsonify(error="unauthorized"), 401
        return view(*args, **kwargs)
    return wrapper

def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        u = current_user()
        if not u:
            return jsonify(error="unauthorized"), 401
        if not u.is_admin:
            return jsonify(error="forbidden"), 403
        return view(*args, **kwargs)
    return wrapper

def log_action(op, table, message, user_id=None):
    db.session.add(AuditLog(op=op, table_name=table, message=message, user_id=user_id))

def get_json():
    return request.get_json(silent=True) or {}

def clean_text(value, max_len=2000):
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return s

    s = "".join(c for c in s if c == "\n" or c == "\r" or c == "\t" or ord(c) >= 32)
    return s[:max_len]
