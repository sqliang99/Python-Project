""""
History Price Data Clean
author : Iris Shi
""""
import pandas as pd
import time
df = pd.read_csv('./gamesprices-ggdeals（HdataIncluded）.csv')
df.drop_duplicates(inplace = True)
df.drop_duplicates(subset=['Title','Original Price'],inplace = True)

reocord_time = []
price = []
shop = []
duration = []
d = df.set_index('Title')['Hchart'].to_dict()

history = pd.DataFrame()
for k,v in d.items():
    print(k)
    q = v.split('{')
    del q[0 : 2]
    df_temp = pd.DataFrame()
    for i in q:
        temp = i.split(',')
        temp.pop()
        dur = temp.pop().replace(" 'name': '","").replace("'}","").replace("]","")
        temp1 = []
        for n in temp:
            tem = n.split(':')
            for t in tem:
                temp1.append(t.replace("'","").strip())
        time0 = int(temp1[1])
        tre_timeArray = time.localtime(time0/1000)
        time0 = time.strftime("%Y-%m-%d %H:%M:%S", tre_timeArray)
        price0 = temp1[3]
        shop0 =temp1[5]
        reocord_time.append(time0)
        price.append(price0)
        shop.append(shop0)
        duration.append(dur)
    df_temp['time'] = reocord_time
    df_temp['price'] = price
    df_temp['shop'] = shop
    df_temp['duration'] = duration
    df_temp['name'] = k
    history = pd.concat([history, df_temp])
	
history.to_csv('./history.csv',index = False)