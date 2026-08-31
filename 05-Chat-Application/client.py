import asyncio
import websockets

async def chat_client():
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        print("Connected to chat server. Type messages (Ctrl+C to quit):")
        while True:
            msg = input("You: ")
            await websocket.send(msg)
            reply = await websocket.recv()
            print("Other:", reply)

asyncio.run(chat_client())
