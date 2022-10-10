import streamlit as st
import pandas as pd
import re
import price_compare as f
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy
import openpyxl
import process_history

st.title("Pricer Killer")
st.subheader("play cheaper, play happier", anchor=None)
st.write('Note: you don\'t have to worry about capitalization or punctation, but you need to enter the full name!')
st.write('For example, if you want to look at Civ V, you need to enter \"Sid Meier\'s Civilization® V\"')
title_input = st.text_input('What game are you looking for?', 'Hades')
if title_input:
    st.write('You are looking for the game: ', title_input)

    title = re.sub('[^A-Za-z0-9 ]+', '', title_input)
    title = title.lower()

    steam = pd.read_csv('gamesprices.csv')
    nintendo = pd.read_csv('gamesprices-Nintend(full).csv')
    gg = pd.read_excel('cleaned_ggdeal.xlsx')
    steam, nintendo, gg = f.data_processing(steam, nintendo, gg)
    history = pd.read_csv('sub_price_history.csv')
    history = process_history.make_history(history)

    if f.find_game(title, steam, nintendo, gg):

        df1, platform, pr, message = f.price_comparison(title, steam, nintendo, gg)
        st.write('The current cross-platform lowest price is', pr,'on', ','.join(platform))
        if len(message) > 0 :
            for line in message:
                st.write(line)
        df2 = pd.DataFrame(df1.stack()).reset_index()
        df2 = df2.rename(columns = {'level_1':'platform', 0:'price'})
        df2 = df2.drop('level_0', axis = 1)

        st.dataframe(df1.style.highlight_min(axis=1))

        if st.button('comparison plot'):
            fig = plt.figure(figsize=(10, 4))
            ax = fig.add_subplot(111)
            bars = ax.barh(df2['platform'], df2['price'])
            ax.bar_label(bars)
            ax.set_ylabel('price')
            st.pyplot(fig)

        if title in set(history['name']):
            st.write('We found price history for this game, would you like to see it?')
            if st.button('Yes!'):
                temp = process_history.make_temp(title, history)
                fig, ax = plt.subplots()
                sns.lineplot(ax = ax, x="time_int", y="price", hue='shop',
                             data=temp)
                # get current axis
                ax = plt.gca()
                # get current xtick labels
                xticks = ax.get_xticks()
                # convert all xtick labels to selected format from ms timestamp
                ax.set_xticklabels([pd.to_datetime(tm, unit='s').strftime('%Y-%m-%d\n %H:%M:%S') for tm in xticks],
                                   rotation=50)
                st.pyplot(fig)

    else:
        st.write('Sorry, we don\'t have data on the game you are looking for!')
