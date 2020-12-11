import asyncio
import json
import uuid
import websockets

users = []
print()


class User:

    def __init__(self, web):
        self.web = web
        self.uuid = uuid.uuid4()


async def hello(websocket, path):
    cur_user = User(websocket)
    users.append(cur_user)
    print("connected")
    while True:
        data = await websocket.recv()
        loaded = json.loads(data)
        loaded["isMyMessage"] = False
        loaded["key"] = str(cur_user.uuid)
        loaded["message"]["isMyMessage"] = False
        print("GOT DATA", data)
        for user in users.copy():
            if cur_user.uuid != user.uuid:
                print("SENDING TO", user)
                try:
                    await user.web.send(json.dumps(loaded))
                except Exception as e:
                    users.remove(user)
                    pass


start_server = websockets.serve(hello, "127.0.0.1", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
