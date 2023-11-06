import asyncio
import websockets
from websockets.server import serve

connected_clients = set()

async def handle_client(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
            await broadcast_message(message)
    except websockets.exceptions.ConnectionClosedOK as e:
        print(f"Connection closed with status code 1000: {e}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    finally:
        connected_clients.remove(websocket)

async def broadcast_message(message):
    if connected_clients:
        await asyncio.gather(*[client.send(message) for client in connected_clients])

async def main():
    async with serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())