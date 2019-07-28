

SIMPLE_APP = {
    'app.py': """\
from sanic import Sanic
from sanic.response import text

def register_routes(app):
    @app.route('/')
    async def hello(request):
        return text('hello world')

def create_app():
    app = Sanic()
    register_routes(app)
    return app"""
}
