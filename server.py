import asyncio

import websockets
from aiohttp import web

async def handler(websocket, path):
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.ConnectionClosed:
        print("Client disconnected")

async def health(request):
    return web.Response(text="OK", status=200)


async def main():
        ws_server = websockets.serve(handler, "localhost", 8765)
        print("WebSocket server started on ws://localhost:8765")

        # Start HTTP server for health checks
        app = web.Application()
        app.add_routes([web.get('/health', health)])
        runner = web.AppRunner(app)

        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8766)
        # Run both servers concurrently
        await asyncio.gather(
            ws_server,
            site.start(),
        )
        print("WebSocket and http server started")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
