from flask import Config
import os

from app.utils import constants


def create_app(config_class=Config):
    from flask import Flask
    app = Flask("recallr",
                template_folder="app/templates",
                static_folder="app/static")
    app.config.from_object(config_class)

    if not os.path.exists(constants.DECK_PATH):
        os.mkdir(constants.DECK_PATH)


    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    from .routes.deck import deck_bp
    app.register_blueprint(deck_bp)

    from .routes.card import card_bp
    app.register_blueprint(card_bp)

    return app
