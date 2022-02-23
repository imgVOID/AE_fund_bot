from .send_alert import send_alert_vandals
from json import loads


async def websocket_server_start(websocket):
    data = loads(await websocket.recv())
    username = data.get("username")
    region_name = data.get("region_name")
    await send_alert_vandals(username, region_name)
