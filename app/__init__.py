from flask import Config
import os
from app.utils import constants
from app.services.db import init_db, init_db_data


def create_app(config_class=Config):
    from flask import Flask
    app = Flask("recallr",
                template_folder="app/templates",
                static_folder="app/static")
    app.config.from_object(config_class)

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

    return app
