from flask import Config

def create_app(config_class=Config):
    from flask import Flask
    app = Flask("recallr",
                template_folder="app/templates",
                static_folder="app/static")
    app.config.from_object(config_class)


    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    from .routes.card import card_bp
    app.register_blueprint(card_bp)

    return app
