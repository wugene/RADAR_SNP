
# coding: utf-8

# In[2]:


# %load AE_2nd_prep.py


# In[1]:


import gzip, pickle

G_f_src = "AE1_out.pkl.gz"
G_f_tar = "AE2_in.pkl.gz"

def load_data(fn):
    with gzip.open(fn) as f:
        return pickle.load(f)
    
def save_data(d, fn):
    with gzip.open(fn, "w") as f:
        pickle.dump(d, f)


# In[2]:


(G_k, G_x, G_y) = load_data(G_f_src)


# In[3]:


import pandas as pd
from pandas import DataFrame as df

def encode_to_df(k, x, y):
    x_all = dict()
    y_all = dict()
    
    for k_1, x_1, y_1 in zip(k, x, y):
        c_1, d_1 = k_1
        
        if d_1 not in x_all:
            x_all[d_1] = dict()
            y_all[d_1] = dict()
        
        x_all[d_1][c_1] = x_1
        y_all[d_1][c_1] = y_1
        
    x_df = df.from_dict(x_all)
    y_df = df.from_dict(y_all)
   
    return x_df, y_df


# In[4]:


G_x_df, G_y_df = encode_to_df(G_k, G_x, G_y)


# In[5]:


def is_nan_in_df(df_all):
    cols = df_all.columns
    for cn_1 in cols:
        for c_1, x_1 in df_all[cn_1].iteritems():
            if (len(x_1) < 10):
                print ("Missing in %s, %s" % (cn_1, c_1))
                return True
    return False


# In[6]:


is_nan_in_df(G_x_df)


# In[7]:


import numpy as np

# (date, code, encoded_num) => (date, encoded_num, code)
def dim_convert(df_x):
    d_s = df_x.columns
    c_s = df_x.index
    
    x_all = dict()
    for d_1 in d_s:
        
        x_1 = list()
        ind = 0
        for c_1 in c_s:
            x_1.append(df_x[d_1][c_1])
        
        x_all[d_1] = dict()
        x_t = np.transpose(x_1)
        for i in range(len(x_t)):
            x_all[d_1][i] = x_t[i]
    
    return df.from_dict(x_all, orient='index')


# In[8]:


G_x_df_T = dim_convert(G_x_df)


# In[9]:


print (G_x_df_T.columns)
print (G_x_df_T.index)


# In[10]:


G_data_ae3 = (G_x_df_T, G_y_df)
save_data(G_data_ae3, G_f_tar)


