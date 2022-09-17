"""Fetch structured JSON-LD data from a given URL."""
from pprint import pprint
import requests
import extruct
import pandas as pd
from bs4 import BeautifulSoup
# text=requests.get('https://www.dekudeals.com/hottest?view=list').text

# def import_data(url):
#     r = requests.get(url)
#     #read json as a dictoinary
#     data = dict(r.json())
#     return data['results_html']

def parse(data):
    gamelist=[]
    main_page = BeautifulSoup(data, "html.parser")
    games=main_page.find_all('div',{'class':'w-100 items-list-row'})
    for game in games:
        if game.find('a',{'class':"main-link"}) is not None:
            title = game.find('a', {'class': "main-link"}).text.strip()
        if game.find('small') is not None:
            sale_end_date=game.find('small').text
        else:
            sale_end_date="NA"
        originalPrice=game.find('s',{'class':'text-muted'}).text
        # print(currentPrice)
        currentPrice=game.find('strong').text
        discount=game.find('span',{'class':'badge badge-danger'}).text
        if game.find('span',{'class':'badge badge-warning'}) is not None:
            priceStatus=game.find('span',{'class':'badge badge-warning'}).text
        else:
            priceStatus="NA"
        Mygame={
            'title':title,
            'Original Price':originalPrice,
            'Current Price':currentPrice,
            'Discount':discount,
            'Sale End Date':sale_end_date,
            'Price Status':priceStatus
        }
        gamelist.append(Mygame)
    return gamelist
results = []
for x in range(1,43,1):
    url="https://www.dekudeals.com/hottest?view=list&page="
    url1=url+str(x)
    data=requests.get(url1).text
    results.append(parse(data))
    # a=pd.concat([pd.DataFrame(results) for g in results])
    # print(a)
gamesdf = pd.concat([pd.DataFrame(g) for g in results])
# print(results)
gamesdf.to_csv('gamesprices-Nintend.csv', index=False)

# data=requests.get('https://www.dekudeals.com/hottest?view=list&page=2').text
# results.append(parse(data))
# print(results)

# print(gamesdf)
# # # ,columns=['Title','Original Price','Current Price', 'Discount','Sale End Date','Price Status']

# print('Fin. Saved to CSV')
# print(gamesdf)

# def output(results):
#     gamesdf = pd.concat([pd.DataFrame(g) for g in results])
#     gamesdf.to_csv('gamesprices.csv', index=False)
#     print('Fin. Saved to CSV')
#     print(gamesdf.head())
#     return
# results = []
# results.append(gamelist)
