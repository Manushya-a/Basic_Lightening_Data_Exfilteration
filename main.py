import asyncio
import websockets
import json

count = int(input("Enter the number of lightning strikes to track: "))

async def fetch_data(count):
    headers = {
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
        "Origin": "https://map.blitzortung.org"
    }
    
    try:
        async with websockets.connect(
            "wss://ws2.blitzortung.org/",
            extra_headers=headers
        ) as ws:
            await ws.send('{"action": "subscribe", "channel": "lightning"}')
            print("Connected and subscribed to lightning channel")
            
            for _ in range(count):
                try:
                    data = await ws.recv()
                    try:
                        # Try to parse JSON data
                        json_data = json.loads(data)
                        print("Received lightning data:", json_data)
                    except json.JSONDecodeError:
                        print("Received non-JSON data:", data)
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed by server")
                    break
                    
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(fetch_data(count))