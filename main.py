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

def flatten(data):
    """
    Converts the List of JSON objects into list of lists that contain the lightening data
    >>> input: List of JSON objects
    >>> output: List of lists 
    """
    ans = []

    for response in data:
        date, resp_time = time_formater(response["time"]).split()
        for individual in response["sig"]:
            temp = []
            temp.append(individual["lat"])
            temp.append(individual["lon"])
            temp.append(date)
            temp.append(resp_time + time_formater(individual["time"])) # This doesnt work for now... but ok
            temp.append(individual["sta"])
            temp.append(individual["alt"])
            temp.append(response["mds"])
            temp.append(response["mcg"])
            temp.append(response["region"])
            temp.append(response["delay"])

            ans.append(temp)

    return ans

def time_formater(time):
    """
    Converts the Unix timestamp into time in form of DD-MM-YYYY HH-MM-SS
    >>> input: String of unix time
    >>> output: String of time value 
    """
    ts_seconds = time / 1e9  # Convert to seconds
    dt = datetime.fromtimestamp(ts_seconds)

    return str(dt)

count = int(input("Enter the number of lightning strikes to track: "))

def decode(b):
    """
    Function reverse engineered from the website that take
    >>> input: Encoded string of data
    >>> output: Decoded string
    """
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

async def main():
    """
    Start point of the code
    """
    parser = argparse.ArgumentParser(description="Output the required data in differnt modes")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-log", action="store_true", help="Run in log mode")
    group.add_argument("-excel", action="store_true", help="Run in Excel mode")
    group.add_argument("-gsheet", action="store_true", help="Run in Google sheet mode")
    
    parser.add_argument("number", type=int, help="Number of responses you want to intercept")
    
    args = parser.parse_args()

    data = await fetch_data(args.number)
    
    if args.log:
        log_mode(data)
    elif args.excel:
        excel_mode(data)
    elif args.gsheet:
        gsheet_mode(data)

if __name__ == "__main__":
    print(bcolors.HEADER + ">>>> Initialising....." + bcolors.ENDC)
    asyncio.run(main())
    print(bcolors.HEADER + ">>>> Concluding Execution" + bcolors.ENDC)