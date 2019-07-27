from sanic import Sanic
from sanic.response import json


def register_routes(app):
    @app.route('/')
    async def test(request):
        return json({'hello': 'world1'})


def create_app():
    app = Sanic("devtools-demo")
    register_routes(app)
    return app
