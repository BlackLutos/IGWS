import asyncio
import websockets
async def hello(uri,data):
    async with websockets.connect(uri) as websocket:
        await websocket.send(data)
        print("(client) send to server: " + data)
        name = await websocket.recv()
        print("(client) recv from server " + name)
flag = True
while(flag):
    n = input()
    asyncio.get_event_loop().run_until_complete(
    hello('ws://172.30.1.32:8848',n))
    if n == '0':
        flag = False


# asyncio.get_event_loop().run_until_complete(
#     hello('ws://localhost:8765'))