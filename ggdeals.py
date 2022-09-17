"""
web scraping game prices from gg deals

"""

import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://gg.deals/deals/"

text = requests.get(url).text
games_raw = BeautifulSoup(text, 'html.parser')
gamelist = []
games_wrapper = games_raw.find('div', {'class': 'd-flex flex-wrap relative list-items shadow-box-small-lighter'})
games = games_wrapper.findChildren()

for game in games:
    title_wrapper = game.find('div', {'class': 'game-info-title-wrapper'})
    if title_wrapper is not None:
        title = title_wrapper.find('a').text.strip()
    price_wrapper = game.find('div', {'class': 'price-wrapper with-badges'})
    if price_wrapper is not None:
        price_old = game.find('span', {'class': 'price-label price-old'}).text.strip()
        price_new = game.find('span', {'class': 'price-inner game-price-new'}).text.strip()

    game = {
        'title': title,
        'Original Price': price_old,
        'New Price': price_new
    }
    gamelist.append(game)

games_df = pd.DataFrame(gamelist)
games_df.to_csv('gameprices-ggdeals.csv', index=False)

#name_wrapper = game.find('div', {'class': 'game-info-title_wrapper'})
#print(name_wrapper)
#print(bsyc.prettify())
#fout = open('bsyc_temp.txt', 'wt', encoding='utf-8')
#fout.write(str(bsyc))
#fout.close()

