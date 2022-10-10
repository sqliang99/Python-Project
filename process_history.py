import pandas as pd
import re
import price_compare as f
import matplotlib.dates as mdates

def make_temp(title, history):
    temp = history[history['name'] == title]
    temp = temp.sort_values('date', ascending=False)
    temp = temp.head(200)

    return temp

def make_history(history):
    def time_to_int(dateobj):
        total = int(dateobj.strftime('%S'))
        total += int(dateobj.strftime('%M')) * 60
        total += int(dateobj.strftime('%H')) * 60 * 60
        total += (int(dateobj.strftime('%j')) - 1) * 60 * 60 * 24
        total += (int(dateobj.strftime('%Y')) - 1970) * 60 * 60 * 24 * 365
        return total

    history['name'] = history['name'].apply(lambda mystring: re.sub('[^A-Za-z0-9 ]+', '', mystring))
    history['name'] = history['name'].apply(lambda x: x.lower())
    history['name'] = history['name'].apply(lambda x: x.strip())
    history['price'] = pd.to_numeric(history.price, errors='coerce')
    history['time'] = pd.to_datetime(history['time'], format='%Y-%m-%d %H:%M:%S')
    history['date'] = history['time'].dt.date
    history = history.groupby(['name', 'date', 'shop']).price.min().rename('price').reset_index()
    history['time_int'] = history['date'].apply(lambda x: time_to_int(x))
    return history