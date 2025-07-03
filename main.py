import asyncio
import websockets  # Install with: pip install websockets
import json

count = int(input("Enter the number of lightning strikes to track: "))

async def fetch_data(count):
    header = {
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'Origin': 'https://map.blitzortung.org'
    }
    async with websockets.connect("wss://ws2.blitzortung.org/", additional_headers = header) as ws:
        await ws.send('{"action": "subscribe", "channel": "lightning"}')
        for _ in range(count):
            print("trying to fetch data")
            #data = json.loads(await ws.recv())
            data = await ws.recv()
            print(data)

asyncio.run(fetch_data(count))