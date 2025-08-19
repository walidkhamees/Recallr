from flask import Blueprint, jsonify, render_template, request, redirect
from flask_login import current_user, logout_user

from app.services.auth import login, signup

import app.utils.http_codes as HTTP_CODES

auth_bp = Blueprint("user", __name__, url_prefix="/")

@auth_bp.route("/login", methods=["GET"])
def login_page_route():
    if current_user.is_authenticated:
        return redirect("/deck")
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login_route():
    request_json = request.get_json()
    username = request_json.get("username", "")
    password = request_json.get("password", "")

    if username == "" or password == "":
        return "Error: Username and password are required"

    message = login(username, password)
    if message != "":
        return jsonify({"message": message}), HTTP_CODES.UNAUTHORIZED

    return jsonify({"message": "Logged in successfully"}), HTTP_CODES.OK

@auth_bp.route("/logout", methods=["GET"])
def logout_route():
    logout_user()
    return redirect("/")

@auth_bp.route("/signup", methods=["GET"])
def signup_page_route():
    if current_user.is_authenticated:
        return redirect("/deck")
    return render_template("signup.html")

@auth_bp.route("/signup", methods=["POST"])
def signup_route():
    request_json = request.get_json()

    username = request_json.get("username", "")
    password = request_json.get("password", "")
    confirm_password = request_json.get("password_confirm", "")

    message = signup(username, password, confirm_password)
    if message != "":
        return jsonify({"message": message}), HTTP_CODES.BAD_REQUEST

    return jsonify({"message": "Signed up successfully"}), HTTP_CODES.OK
