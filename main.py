import argparse
import asyncio
import websockets
import json
import sys
import time
import gspread

from datetime import datetime
from openpyxl import Workbook
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError

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
    """
    Fetches data from the target asynchronously
    
    >>>> returns: A list with json objects inside  
    """
#    headers = {  I initially thought this was necessary to get the request through but i guess not
#        "Pragma": "no-cache",
#        "Cache-Control": "no-cache",
#        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
#        "Origin": "https://website.url"
#    }

    try:
        main_data = []
        async with websockets.connect("wss://websocket.link/") as ws:
            await ws.send('{"'+'a'+'":'+'111'+'}')
            print(bcolors.ORANGE + "[" + str(datetime.now()) + "]" + bcolors.ENDC + bcolors.BOLD +" Connected and subscribed to lightening channel" + bcolors.ENDC)
            
            for _ in range(count):
                try:
                    data = await ws.recv()
                    try:
                        
                        # Try to parse JSON data
                        print(bcolors.ORANGE + "[" + str(datetime.now()) + "]" + bcolors.OKGREEN + " Received lightening data" + bcolors.ENDC)

                        main_data.append(json.loads(decode(data).replace("'", '"')))

                    except json.JSONDecodeError:
                        print(bcolors.RED + "Received non-JSON data:" + bcolors.ENDC)
                        print(decode(data))
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed by server")
                    print(bcolors.RED + "Connection closed by server" + bcolors.ENDC)
                    break
        return main_data

    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(fetch_data(count))