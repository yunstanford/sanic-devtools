from .test1 import test_api_1
from .test2 import test_api_2

def register_routes(app):
    app.add_route(test_api_1, "/api/v1/test1/", methods=["GET"])
    app.add_route(test_api_2, "/api/v1/test2/", methods=["GET"])
