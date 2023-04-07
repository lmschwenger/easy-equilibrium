from flask import Flask

from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from easy_equilibrium.processing.routes import equilibrium_page
    app.register_blueprint(equilibrium_page)

    return app
