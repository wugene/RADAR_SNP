
# coding: utf-8

# In[1]:


import gzip, pickle

def load_data(fn):
    with gzip.open(fn) as f:
        d = pickle.load(f)
    return d

def save_data(d, fn):
    with gzip.open(fn, "w") as f:
        pickle.dump(d, f)


# In[2]:


G_f_src = "TEST.pkl.gz"
G_f_tar = "AE.pkl.gz"


# In[3]:


G_hist_raw = load_data(G_f_src)
print(len(G_hist_raw))


# In[ ]:


from scipy import stats
import numpy as np

def x_ae_col_1(col_1):
    
    l = len(col_1)
    
    #get ratio
    col_new = list()
    for i in range(l-1):
        x1 = col_1[i]
        x2 = col_1[i+1]

        r = (x2*1.0)/(x1+x2)
        if (r != r):
            r = 0.5
        col_new.append(r)

    return stats.zscore(col_new)


def x_ae_1(hist_1):
    
    if (len(hist_1)<26):
        return list()
    
    # column-wise processing r=(today/(today+yesterday))
    norm = list()
    for col in hist_1.columns:
        norm.append(x_ae_col_1(hist_1[col]))

    norm_T = np.transpose(norm)

    # flatten 20 lines
    l = len(norm_T)
    x_1 = list()
    for i in range(l-24):
        x_1.append(norm_T[i:i+20].flatten())
    
    return x_1


def k_ae_1(c, hist_1):
    return [(c, i) for i in hist_1.index[20:-5] ]


def y_ae_1(hist_1):
    y_1 = list()
    y_raw = hist_1["Adj Close"]
    l = len(y_raw)
    for i in range(l-25):
        y_new = y_raw[i+24] / (y_raw[i+24] + y_raw[i+20])
        if (y_new != y_new):
            y_new = 0
        else:
            y_new = int((y_new-0.52)/100.0+1.0) # 1 if y_new>0.52
            
        y_1.append(y_new)
        
    return y_1



def kxy_ae(hist_all):
    
    #check blank
    max_len = 0
    for c in hist_all.keys():
        k_1 = k_ae_1(c, hist_all[c])
        if (max_len < len(k_1)):
            max_len = len(k_1)
    
    x_all, y_all, k_all = list(), list(), list()
    for c in hist_all.keys():
        k_1 = k_ae_1(c, hist_all[c])
        if (max_len == len(k_1)):
            k_all.extend(k_1)
            x_all.extend(x_ae_1(hist_all[c]))
            y_all.extend(y_ae_1(hist_all[c]))

    return (k_all, x_all, y_all)


# In[ ]:


G_data_ae = kxy_ae(G_hist_raw)


# In[ ]:


print(len(G_data_ae[0]), len(G_data_ae[1]), len(G_data_ae[2]))
print(sum(G_data_ae[2])/len(G_data_ae[2]))


# In[ ]:


save_data(G_data_ae, G_f_tar)

