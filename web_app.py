
from flask import Flask
from src.restful_app import restful_api
from extensions import session


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    restful_api(app)
    session.init_app(app)
    return app


app = create_app()
