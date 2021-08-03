import requests
import os

html = os.environ["data"]
html1 = os.environ["data 1"]
html2 = os.environ["data 2"]


async def get(channel_id):
    return requests.get(html).json()["user"][str(channel_id)]


async def put(channel_id, add_data):
    data = requests.get(html).json()
    data["user"][str(channel_id)] = add_data
    return requests.put(html1, params={"id": html2}, json=data).json()


async def get_all():
    return requests.get(html).json()


async def put_all(data):
    return requests.put(html1, params={"id": html2}, json=data).json()


async def create_new_data(ctx):
    data = requests.get(html).json()
    data["user"][str(ctx.channel.id)] = {"name": ctx.channel.name, "materials": {}, "edit": True}
    return requests.put(html1, params={"id": html2}, json=data)


async def check_more(channel_id: str):
    data = requests.get(html).json()
    for materials in data["user"][str(channel_id)]["materials"]:
        if int(data["user"][str(channel_id)]["materials"][materials]) <= 0:
            data['user'][str(channel_id)]["materials"].pop(materials, None)
    return requests.put(html1, params={"id": html2}, json=data)
