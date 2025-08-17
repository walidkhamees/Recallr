from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, logout_user

from app.services.auth import login, sign_up

auth_bp = Blueprint("user", __name__, url_prefix="/")

@auth_bp.route("/login", methods=["GET"])
def login_page_route():
    if current_user.is_authenticated:
        return redirect("/deck")
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login_route():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    print(username, password)

    if username == "" or password == "":
        return "Error: Username and password are required"

    message = login(username, password)
    print(message)
    if message != "":
        flash(message)
        return redirect("/login")

    return redirect("/deck")

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
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    confirm_password = request.form.get("password_confirm", "")

    print("username ", username)
    print("password ", password)

    if password != confirm_password:
        flash("Error: Passwords do not match")
        return redirect("/signup")

    message = sign_up(username, password)
    if message != "":
        flash(message)
        return redirect("/signup")

    return redirect("/login")
