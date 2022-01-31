from webbrowser import get
import requests
from pandas import json_normalize 
from datetime import datetime, timedelta
import os
import aiohttp
import asyncio
from secrets import API_KEY_POLYGON as token

# How many days we wanna look back
days = 730

# Get the tickers from Polygon
def return_commonstock_tickers(token):
    url = 'https://api.polygon.io/v3/reference/tickers'
    
    parameters = {
        'apiKey': token, # your API key
        'type': 'CS', # query common stocks
        'market': 'stocks',
        'limit': 1000 # extract max data possible
    }

    try:
        tickers_json = requests.get(url, parameters).json()
        tickers_list = tickers_json['results']
        
        while tickers_json['next_url']:
            tickers_json = requests.get(tickers_json["next_url"], parameters).json()
            tickers_list.extend(tickers_json["results"])
            if 'next_url' not in tickers_json.keys():
                break
            
    except:
        return None

    return tickers_list

tickers = return_commonstock_tickers(token)

# write the api response to a csv
def write_csv(data, date, ticker):
    status = data['status']
    path = get_path(date)
        
    # Case when empty file is returned with success 200 response
    if status == 'NOT_FOUND':
        df = json_normalize(data)
        df.to_csv('{}/ERROR/{}_{}.csv'.format(path, ticker, date))

    # Case when requested file is returned with success 200 response
    elif status == 'OK':

        df = json_normalize(data)
        df.to_csv('{}/DONE/{}_{}.csv'.format(path, ticker, date))


# Function to get a list of all dates that are to be downloaded
def get_dates():
    
    # Get earliest date available on POLYGON side
    date_today = datetime.today().date()
    api_date = date_today - timedelta(days) # decide how far back we wanna look 

    # Get last date for which download was done to get start date
    try:
        folder_date = []
        year = max([name for name in os.listdir('output/') if not name.startswith('.')])
        foldernames = os.listdir('output/{}'.format(year))
        folder_CW = [name for name in foldernames if not name.startswith('.')]


        for i in range(len(folder_CW)):
            foldernames = os.listdir('output/{}/{}'.format(year, folder_CW[i]))
            folder_date += [name for name in foldernames if not name.startswith('.')]
        last_date = datetime.strptime(max(folder_date), '%Y-%m-%d').date()
        start_date = max(api_date, last_date + timedelta(days=1))
    except:
        start_date = api_date

    dates = [start_date + timedelta(days=i) for i in range((date_today - start_date).days)]
    todo_dates = [date.strftime('%Y-%m-%d') for date in dates if date.isoweekday() <= 5]
    return(todo_dates)

get_dates()

# Function to get and create a path for the current date
def get_path(date_str):
    
    # Extract year and CW from the date
    date = datetime.strptime(date_str, '%Y-%m-%d')
    year = str(date.year)
    CW = str(date.isocalendar()[1]).rjust(2, '0')
    
    # Check if there exists a folder for this date 
    path = 'output/{}/{}-CW{}/{}'.format(year, year, CW, date_str)
    if not os.path.exists(path):
        os.makedirs(path)
        os.mkdir('{}/ERROR/'.format(path))
        os.mkdir('{}/DONE/'.format(path))
    
    return(path)

# Function to get diff between two numbers
def changePercent(first, second):
    first = round(first, 2)
    second = round(second, 2)
    return ((second - first) / first) * 100

todo_dates = get_dates()

async def main():

    async with aiohttp.ClientSession() as session:

            for i in tickers:
                ticker = i['ticker']
        
                for date in todo_dates:

                    api_url = f'https://api.polygon.io/v1/open-close/{ticker}/{date}?adjusted=true&apiKey={token}'
                    async with session.get(api_url) as resp:
                        data = await resp.json()
                        write_csv(data, date, ticker)               

asyncio.run(main())