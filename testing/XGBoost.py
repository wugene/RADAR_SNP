
# coding: utf-8

# In[1]:


import xgboost as xgb


# In[2]:


dtr = xgb.DMatrix('../xgboost/demo/data/agaricus.txt.train')
dte = xgb.DMatrix('../xgboost/demo/data/agaricus.txt.test')


# In[3]:


params = {'max_depth':2, 'eta':1, 'silent':1, 'objective':'binary:logistic'}
num_round = 2
bst = xgb.train(params, dtr, num_round)


# In[4]:


preds = bst.predict(dte)


# In[6]:


print(preds)

