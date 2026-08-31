import asyncio
import websockets

connected_clients = set()

async def handle_client(websocket):
    connected_clients.add(websocket)
    print("New client connected")
    try:
        async for message in websocket:
            print(f"Message received: {message}")
            # Broadcast to all connected clients
            await asyncio.gather(*[
                client.send(message) for client in connected_clients if client != websocket
            ])
    except websockets.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handle_client, "localhost", 8000):
        print("✅ WebSocket Chat Server running at ws://localhost:8000")
        await asyncio.Future()  # keep running

if __name__ == "__main__":
    asyncio.run(main())
