import requests
import os

html = os.environ["data"]
html1 = os.environ["data 1"]
html2 = os.environ["data 2"]


async def get(channel_id):
    return requests.get(html).json()[str(channel_id)]


async def put(channel_id, data):
    requests.get(html).json()[str(channel_id)] = data
    return requests.put(html1, params={"id": html2}, json=data).json()


async def get_all():
    return requests.get(html).json()
