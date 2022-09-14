"""
web scrap data from steam store's top seller
cap by a certain number

Inspired by https://github.com/jhnwr/steamdeals
"""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1'

def import_data(url):
    r = requests.get(url)
    #read json as a dictoinary
    data = dict(r.json())
    return data['results_html']

def parse(data):
    gameslist = []
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a')
    for game in games:
        title = game.find('span', {'class': 'title'}).text
        price = game.find('div', {'class': 'search_price'}).text.strip().split('$')[1]

        mygame ={
            'title': title,
            'price': price,
        }
        gameslist.append(mygame)
    return gameslist

results = []
limit = 3500

for x in range(0, 3500, 50):
    #scrap 50 games at a time
    data = import_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1')
    results.append(parse(data))
    print('Scraped up to ', x)

gamesdf = pd.concat([pd.DataFrame(g) for g in results])
gamesdf.to_csv('gamesprices.csv', index=False)