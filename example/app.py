from sanic import Sanic
from .routes import register_routes


def create_app():
    app = Sanic("devtools-demo")
    register_routes(app)
    return app
