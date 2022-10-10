#because the original dataset is too big (despite only having 48 games)
#we are going to subset it just so streamlit can run smoothly

import pandas as pd
import numpy as np
import random

full_hist = pd.read_csv('history.csv')
#print(set(full_hist['name']))

result = random.choices(list(set(full_hist['name'])), k=10)

sub = full_hist[full_hist['name'].isin(result)]
sub.to_csv('sub_price_history.csv', index=False)