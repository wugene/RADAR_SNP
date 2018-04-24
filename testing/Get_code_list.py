
# coding: utf-8

# In[2]:


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

code_list = get_kospi200_list()


# In[9]:


import pickle, gzip

with gzip.open("CODE_LIST.pkl.gz", "w") as f:
    pickle.dump(code_list, f)

