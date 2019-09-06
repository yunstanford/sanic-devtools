from sanic.response import json


async def test_api_1(request):
	return json({'hello': 'world1'})