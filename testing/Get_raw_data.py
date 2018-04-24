
# coding: utf-8

# In[1]:


import pickle, gzip

def get_codes():
    with gzip.open("CODE_LIST.pkl.gz") as f:
        c_list = pickle.load(f)

    l = list()
    for c in c_list:
        l.append(c["code"]+".KS")
    
    return l


# In[2]:


G_code_list = get_codes()

#test
#print(len(code_list))


# In[3]:


import pandas_datareader as pdr
from urllib.parse import quote
from datetime import datetime

#TEST
#print (data.DataReader("027410.KS", "yahoo"))


# In[4]:


def get_historical_data(code):
    df = []
    try:
        df = pdr.DataReader(code, "yahoo")
    except:
        print ("Error in \'"+code+"\'")
    return df


# In[9]:


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


# In[10]:


G_history_list = get_dict_of_history(G_code_list)
print(len(G_history_list))


# In[11]:


import pickle, gzip
pickle.dump(G_history_list, gzip.open("TEST.pkl.gz", "wb"))


# In[15]:


import tensorflow as tf

