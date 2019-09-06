from sanic.response import json


async def test_api_2(request):
	return json({'hello': 'world2'})
