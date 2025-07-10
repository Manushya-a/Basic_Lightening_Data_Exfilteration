import asyncio
import websockets
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    ORANGE = '\033[38;5;208m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    MAGENTA = '\033[95m'
    UNDERLINE = '\033[4m'

count = int(input("Enter the number of lightning strikes to track: "))

def decode(b):
    e = {}
    d = list(b)
    c = d[0]
    f = c
    g = [c]
    h = 256
    o = h
    for b in range(1, len(d)):
        a = ord(d[b])
        a = d[b] if h > a else e[a] if a in e else f + c
        g.append(a)
        c = a[0]
        e[o] = f + c
        o += 1
        f = a
    return ''.join(g)

async def fetch_data(count):
#    headers = {  I initially thought this was necessary to get the request through but i guess not
#        "Pragma": "no-cache",
#        "Cache-Control": "no-cache",
#        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
#        "Origin": "https://website.url"
#    }
    
    try:
        async with websockets.connect("wss://websocket.link/") as ws:
            await ws.send('{"'+'a'+'":'+'111'+'}')
            print("Connected and subscribed to lightning channel")
            
            for _ in range(count):
                try:
                    data = await ws.recv()
                    try:
                        # Try to parse JSON data
                        json_data = json.loads(decode(data))
                        print(bcolors.OKGREEN + "Received lightning data:" + bcolors.ENDC)
                        print(json_data)
                    except json.JSONDecodeError:
                        print(bcolors.WARNING + "Received non-JSON data:" + bcolors.ENDC)
                        print(decode(data))
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed by server")
                    print(bcolors.FAIL + "Connection closed by server" + bcolors.ENDC)
                    break
                    
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(fetch_data(count))