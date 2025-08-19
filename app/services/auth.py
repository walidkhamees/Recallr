import re
from flask_login import login_user
from app.services.db import db

from app.utils.functions import hash
from app.model.user import User


def get_user(user_id):
    try:
        get_user_query = "SELECT * FROM user WHERE id = ?"
        user_row = db.fetch_one(get_user_query, (user_id,))
        if user_row is None:
            return None
        user_obj = User(user_row[0], user_row[1], user_row[2])
        return user_obj
    except:
        return None

def signup(username, password, confirm_password):
    try:
        username_pattern = r"^[a-zA-Z0-9]+$"

        if username == "":
            return "Error: Username cannot be empty"
        if len(username) < 5:
            return "Error: Username must be at least 5 characters long"
        if len(username) > 20:
            return "Error: Username must be at most 20 characters long"
        if not re.search(username_pattern, username):
            return "Error: Username can only contain letters and numbers"

        if password.strip() == "":
            return "Error: Password cannot be empty"
        if len(password) < 5:
            return "Error: Password must be at least 5 characters long"
        if len(password) > 20:
            return "Error: Password must be at most 20 characters long"
        if password != confirm_password:
            return "Error: Passwords do not match"


        user_row = db.fetch_one("SELECT * FROM user WHERE username = ?", (username,))
        print("user_row ", user_row)
        if user_row:
            return "Username already exists"


        password_hash = hash(password)
        db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password_hash))
        db.commit()
        return ""
    except:
        return "Error signing up"

def login(username, password):
    user_row = db.fetch_one("SELECT id, username, password FROM user WHERE username = ?", (username,))
    if user_row is None:
        return "Username does not exist"
    if hash(password) != user_row[2]:
        return "Incorrect password"

    user_obj = User(user_row[0], user_row[1], user_row[2])
    login_user(user_obj)

    return ""
