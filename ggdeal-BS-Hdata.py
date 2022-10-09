"""Fetch structured JSON-LD data from a given URL."""
from pprint import pprint
import requests,json
import extruct
import pandas as pd
from bs4 import BeautifulSoup
import re
# def parse(data):
text=requests.get("https://gg.deals/deals/?minRating=0&page=1").text
main_page=BeautifulSoup(text,"html.parser")
gamelist=[]
games_wrapper = main_page.find('div', {'class': 'd-flex flex-wrap relative list-items shadow-box-small-lighter'})
# games = list(set(games_wrapper.findChildren()))
# games=games_wrapper.findChildren()
# games = main_page.find_all('div', {'class': 'hoverable-box'})
games = main_page.find_all("div", 'class'=re.compile("^hoverable-box"))
for game in games:
    # find title
    # if game.find('a', {'class':"game-info-title title tippy-initialized" }) is not None:
    #     title1 = game.find('a', {'class':"game-info-title title tippy-initialized" }).text.strip()
    title_wrapper = game.find('div', {'class': 'game-info-title-wrapper'})
    if title_wrapper is not None:
        title = title_wrapper.find('a').text.strip()
    # find price
    price_wrapper = game.find('div', {'class': 'price-wrapper with-badges'})
    if price_wrapper is not None:
        price_old = game.find('span', {'class': 'price-label price-old'}).text.strip()
        price_new = game.find('span', {'class': 'price-inner game-price-new'}).text.strip()
    if game.find('div',{'class':"time-tag tag"}) is not None:
        timefinder=game.find('div',{'class':"time-tag tag"})
        discountdate=game.find('span',{'class':"title"}).text.strip()
        time=timefinder.find('time',datetime=True)
        if time['datetime'] is not None:
            sdate=time['datetime']
    if game.find('div', {'class': "game-cta shop-icon-cta"}) is not None:
        shopfinder=game.find('div', {'class': "game-cta shop-icon-cta"})
        img=shopfinder.find('img',alt=True)
        store=img['alt']
    # if game.find('div', {'class': "lowest-recorded price-hl price-widget with-bottom d-flex game-labels labels-container"}) is not None:
    #     endtimefinder=game.find('div', {'class': "lowest-recorded price-hl price-widget with-bottom d-flex game-labels labels-container"})
    #     enddate=endtimefinder.find('time',datetime=True)
    #     if enddate['datetime'] is not None:
    #         edate=enddate['datetime']
    if game.find('div', {'class': "game-info-title-wrapper"}) is not None:
        # urlfinder=game.find('div', {'class': "game-image"})
        urlf=game.find('a',{'class': "game-tags game-tags-deal"},href=True)
        url="https://gg.deals"+urlf['href']
        # print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        dataUrl = 'https://gg.deals' + soup.select_one('#historical-chart-container')['data-without-keyshops-url']
        r = requests.get(dataUrl, headers={'X-Requested-With': 'XMLHttpRequest'})
        r.json()['chartData']

    Mygame = {
        'Title': title,
        'Original Price': price_old,
        'New Price': price_new,
        'DiscountDate': sdate,
        # 'EndDate':edate,
        'Store':store,
        'Hchart':r.json()['chartData']
    }
    gamelist.append(Mygame)
    # return gamelist

# for i in range(1,2182,1):
#     result=[]
#     urlnew="https://gg.deals/deals/?minRating=0&page="+str(i)
#     data = requests.get(urlnew).text
#     result.append(parse(data))
# result=[]
# urlnew="https://gg.deals/deals/?minRating=0&page=1"
# data = requests.get(urlnew).text
# result.append(parse(data))
# data="https://gg.deals/deals/?minRating=0"

# gamesdf = pd.concat([pd.DataFrame(g) for g in result])
gamesdf = pd.DataFrame(gamelist)
gamesdf.to_csv('gamesprices-ggdeals.csv', index=False)