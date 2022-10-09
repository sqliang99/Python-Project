import pandas as pd
import numpy as np
import re

def data_processing(steam, nintendo, gg):
    steam = steam.rename(columns={'title': 'game'})
    steam['game'] = steam['game'].apply(lambda mystring: re.sub('[^A-Za-z0-9 ]+', '', mystring))
    steam['game'] = steam['game'].apply(lambda x: x.lower())
    steam = steam.drop_duplicates()

    nintendo = nintendo.rename(columns = {'title':'game'})
    nintendo['game'] = nintendo['game'].apply(lambda mystring: re.sub('[^A-Za-z0-9 ]+', '', mystring))
    nintendo['game'] = nintendo['game'].apply(lambda x: x.lower())
    nintendo = nintendo.drop_duplicates()
    nintendo['Original Price'] = nintendo['Original Price'].apply(lambda x: float(x[1:]))
    nintendo['Current Price'] = nintendo['Current Price'].apply(lambda x: float(x[1:]))

    gg = gg.rename(columns={'game_name': 'game'})
    gg['game'] = gg['game'].apply(lambda mystring: re.sub('[^A-Za-z0-9 ]+', '', mystring))
    gg['game'] = gg['game'].apply(lambda x: x.lower())
    gg['game'] = gg['game'].apply(lambda x: x.strip())
    gg = gg[gg['game'] != '']

    return steam, nintendo, gg

def price_comparison(title, steam, nintendo, gg):
    # first check how many platform is this game on
    plt = []
    price_dic = {}
    add_message = []
    if title in set(steam['game']):
        plt.append('Steam')
        steam_price = float(steam[steam['game'] == title]['price'])
        price_dic['Steam'] = steam_price
    if title in set(nintendo['game']):
        plt.append('Nintendo')
        cur_nin_price = float(nintendo[nintendo['game'] == title]['Current Price'])
        price_dic['Nintendo'] = cur_nin_price
    if title in set(gg['game']):
        for platform in list(gg[gg['game'] == title]['platform']):
            if platform != 'Steam':
                price = float(gg[(gg['game'] == title) & (gg['platform'] == platform)]['new_price'])
                plt.append(platform)
                price_dic[platform] = price

    # lowest price cross platform
    lowest_price = np.min(list(price_dic.values()))
    lowest_platform = [k for k, v in price_dic.items() if v == lowest_price]

    if 'Nintendo' in lowest_platform:
        if nintendo[nintendo['game'] == title].reset_index().loc[0,'Price Status'] == 'Lowest price ever':
            add_message.append('Lowest price ever on Nintendo, get it now!')
        if nintendo[nintendo['game'] == title].reset_index().loc[0,'Price Status'] == 'Matches previous low':
            add_message.append('Current price matches past lowest price on Nintendo')

    price_dic = {k: [v] for (k, v) in price_dic.items()}
    #price_dic['game'] = [title]
    df = pd.DataFrame(price_dic)
    #df = df[['game'] + [x for x in df.columns if x != 'game']]
    return df, lowest_platform, lowest_price, add_message

def find_game(title,steam, nintendo, gg):
    all_game = set(steam['game']).union(set(nintendo['game'])).union(set(gg['game']))
    if title in all_game:
        return True
    else:
        return False
