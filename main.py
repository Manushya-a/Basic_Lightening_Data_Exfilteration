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

def input_to_file(data):
    """
    Creates a .xlsx file and input the value into it
    >>> input: List of lists of data
    >>> output: returns the timestamp of the moment the file was stored
    """
    flattened_data = flatten(data)
    wb = Workbook()
    ws = wb.active
    ws.title = "Lightening data"

    # Add headers if needed
    headers = ["lat", "lon", "date", "time", "sta",	"alt", "mds", "mcg", "region", "delay"]
    ws.append(headers)

    # Add all data at once
    for row in flattened_data:
        ws.append(row)

    # Save the workbook
    time_stamp = str(datetime.now()) + ".xlsx"
    wb.save(time_stamp)

    return time_stamp

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

def log_mode(data):
    """
    Prints the data into the shell
    >>> input: List of JSON objects to be stored
    >>> output: NA
    """
    print(bcolors.ORANGE + "[" + str(datetime.now()) + "]" + bcolors.OKCYAN + " Entering: LOG MODE" + bcolors.ENDC)
    print(bcolors.OKBLUE + "Requested Lightening data: " + bcolors.ENDC)
    time.sleep(2)
    print(data)

def excel_mode(data):
    """
    Stores the data into a .xlsx file
    >>> input: List of JSON objects to be stored
    >>> output: NA
    """
    print(bcolors.ORANGE + "[" + str(datetime.now()) + "]" + bcolors.OKCYAN + " Entering: EXCEL MODE" + bcolors.ENDC)
    print(bcolors.OKBLUE + "Output file is stored as : " + bcolors.ENDC + bcolors.BOLD + input_to_file(data) + bcolors.ENDC)

def gsheet_mode(data):
    """
    Connects to the Google cloud using API call and stores the data on the spreadsheet
    >>> input: List of JSON objects to be stored in a Google spreadsheet
    >>> output: NA
    """

    flattened_data = flatten(data)

    print(bcolors.ORANGE + "[" + str(datetime.now()) + "]" + bcolors.OKCYAN + "Entering: GOOGLE SHEET MODE" + bcolors.ENDC)

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    try:
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)
    except Exception as e:
        print(bcolors.ORANGE + "[" + str(datetime.now()) + "]" + bcolors.RED + " An error occured while verifying credentials." + bcolors.ENDC)
        print(bcolors.RED + "Error : " + bcolors.ENDC + str(e))
        sys.exit(1)

    sheets_id = "Link-to-your-google-spreadsheet" 
    workbook = client.open_by_key(sheets_id)
    sheet = workbook.sheet1

    print(bcolors.ORANGE + "[" + str(datetime.now()) + "]" + bcolors.OKGREEN + " Connection established!" + bcolors.ENDC)
    print(bcolors.ORANGE + "[" + str(datetime.now()) + "]" + bcolors.OKGREEN + " Outputing to Google Sheet with the id: "+ bcolors.ENDC + bcolors.BOLD + sheets_id + bcolors.ENDC)

    for i in range(len(flattened_data)):
        for j in range(len(flattened_data[i])):
            sheet.update_cell(i + 2, j + 1, flattened_data[i][j])
            time.sleep(0.75)

    print(bcolors.ORANGE + "[" + str(datetime.now()) + "]" + bcolors.OKGREEN + " Output complete" +  bcolors.ENDC)

def decode(b):
    """
    Function reverse engineered from the website that takes
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