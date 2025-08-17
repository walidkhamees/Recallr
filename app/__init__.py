import os
from flask import Config, render_template
from flask_login import LoginManager
from dotenv import load_dotenv

from app.utils import constants
from app.services.db import init_db, init_db_data


def create_app(config_class=Config):
    try:
        load_dotenv()
    except Exception as e:
        raise Exception(f"Error loading .env file: {e}")

    from flask import Flask
    app = Flask("recallr",
                template_folder="app/templates",
                static_folder="app/static")
    app.config.from_object(config_class)
    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    try:
        if not os.path.exists(constants.DB_PATH):
            with open(constants.DB_PATH, "w") as db_file:
                db_file.write("")
        if not os.path.exists(constants.RESULTS_PATH):
            os.mkdir(constants.RESULTS_PATH)
    except Exception as e:
        raise Exception(f"Error creating database file: {e}")

    init_db()
    init_db_data()


    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.services.auth import get_user
        return get_user(user_id)

    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    from .routes.deck import deck_bp
    app.register_blueprint(deck_bp)

    from .routes.card import card_bp
    app.register_blueprint(card_bp)

    from .routes.quiz import quiz_bp
    app.register_blueprint(quiz_bp)

    from .routes.result import result_bp
    app.register_blueprint(result_bp)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    @app.errorhandler(404)
    def page_not_found(_):
        error = {
            "title": "404 Not Found",
            "message": "The page you are looking for does not exist."
        }
        return render_template("error.html", error=error), 404

    @app.errorhandler(401)
    def page_not_authorized(_):
        error = {
            "title": "401 Unauthorized",
            "message": "You are not authorized to access this page."
        }
        return render_template("error.html", error=error), 401

    return app
