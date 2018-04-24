
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def get_sector(code):
    url = 'http://finance.naver.com/item/main.nhn?code=' + code
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    sector = ""
    h4 = soup.find('h4', {'class':'h_sub sub_tit7'})

    if h4 is not None:
        sector = h4.a.text
    return sector

def get_kospi200_list():
    stock_list = []

    for c in range(1,21):
        rank = 0;
        url = 'http://finance.naver.com/sise/entryJongmok.nhn?page=' + (str)(c)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        table = soup.find("table", {"class":"type_1"})
        rows = table.find_all('tr')
        for row in rows:
            stock = {}
            get_stock = row.find_all('td', {'class':'ctg'})
            if len(get_stock) != 0:
                rank += 1
                stock['rank'] = (c-1)*10 + rank
                stock['name'] = get_stock[0].text
                stock['code'] = get_stock[0].find('a').get('href').split('=')[1]

            get_stock_amount = row.find_all('td', {'class':'number_2'})
            if len(get_stock_amount) != 0:
                stock['total_amount_of_market_price'] = get_stock_amount[3].text
            if len(get_stock) != 0:
                stock['sector'] = get_sector(stock['code'])
                stock_list.append(stock)

    return stock_list


# In[2]:


code_list = get_kospi200_list()


# In[3]:


import pickle, gzip

def get_codes(c_list):
    l = list()
    for c in c_list:
        l.append(c["code"]+".KS")
    
    return l


# In[4]:


G_code_list = get_codes(code_list)

#test
#print(len(code_list))


# In[6]:


import pandas_datareader as pdr
from urllib.parse import quote
from datetime import datetime

#TEST
#print (data.DataReader("027410.KS", "yahoo"))


# In[7]:


def get_historical_data(code):
    df = []
    try:
        df = pdr.DataReader(code, "yahoo")
    except:
        print ("Error in \'"+code+"\'")
    return df


# In[8]:


def get_dict_of_history(codes):
    
    all_data = dict()

    for code in codes:
        data = get_historical_data(code)
        if len(data)>0:
            #print(code, str(len(data)))
            all_data[code] = data
            print("#", end="")

    print ("END!!")

    #test
    #print(all_data[codes[7]][0:5])
    
    return all_data


# In[9]:


G_history_list = get_dict_of_history(G_code_list)
print(len(G_history_list))


# In[5]:


import pickle, gzip
pickle.dump(G_history_list, gzip.open("AE0_raw.pkl.gz", "wb"))


# In[15]:


import tensorflow as tf

