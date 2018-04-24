
# coding: utf-8

# In[2]:


from pandas import DataFrame
import numpy as np
import gzip
import _pickle as pkl


# In[20]:


def get_shuffled_and_mutated(snp, false_set, randoms):

    a_snp = list()
    for kind_np in snp:
        if (false_set):
            np.random.shuffle(kind_np)
        a_snp.extend(kind_np)

    len_a_snp = len(a_snp)

    #add random 1 noise
    for _ in range(randoms):
        rand_pos = np.random.randint(len_a_snp)
        a_snp[rand_pos] = 1

    return a_snp


# In[21]:


def array_for_a_group(group, false_set, randoms):

    a_group = list()
    for snp in group:
        a_group.append(get_shuffled_and_mutated(snp, false_set, randoms))

    len_a_group = len(a_group)
    group_np = np.pad(a_group, [[0,30-len_a_group],[0,0]], 'edge')

    return group_np


# ### <font color=red>WARNING</font> original data of m_pkl will be shuffled
# ### if you call with false_set=True option

# In[22]:


def make_a_set(m_pkl, false_set=False, randoms=10):

    k_set = list()
    d_set = list()

    for key, group in m_pkl.items():
        k_set.append(key)
        d_set.append(array_for_a_group(group, false_set, randoms))

    return k_set, d_set


# In[30]:


def make_multiple_sets(m_pkl, n_sets=10):
    true_sets = list()
    false_sets = list()
    key_set = list()

    print("Create true set %d" % (0))
    k, d = make_a_set(m_pkl, randoms=0)
    true_sets.extend(d)
    key_set.extend(k)
    for idx in range(1, n_sets):
        print("Create true set %d" % (idx))
        _, d = make_a_set(m_pkl)
        true_sets.extend(d)

    #WARNING original data of m_pkl will be shuffled
    for idx in range(n_sets):
        print("Create false set %d" % (idx))
        _, d = make_a_set(m_pkl, false_set=True)
        false_sets.extend(d)
        
    return true_sets, false_sets, key_set


# In[36]:


def read_datafile(set_permut=0):

    permut_array = [ [ 0, 1, 2 ],
                     [ 0, 2, 1 ],
                     [ 1, 0, 2 ],
                     [ 1, 2, 0 ],
                     [ 2, 0, 1 ],
                     [ 2, 1, 0 ] ]

    n_tr, n_vl, n_pr = permut_array[ set_permut % 6 ]

    pkl_f = 'PKL/true_set_merged.pkl.gz'
    split_3 = pkl.load(gzip.open( pkl_f, 'rb'))
    m_tr, _    = split_3[n_tr]
    m_vl, _    = split_3[n_vl]
    m_pr, l_pr = split_3[n_pr]

    X_tr_T, X_tr_F, _    = make_multiple_sets(m_tr, 30)
    X_vl_T, X_vl_F, _    = make_multiple_sets(m_vl, 1)
    X_pr_T, X_pr_F, K_pr = make_multiple_sets(m_pr, 1)

    Y_tr = np.array([1] * len(X_tr_T) + [0] * len(X_tr_F))
    Y_vl = np.array([1] * len(X_vl_T) + [0] * len(X_vl_F))
    
    X_tr = np.array( X_tr_T + X_tr_F )
    X_vl = np.array( X_vl_T + X_vl_F )
    X_pr = np.array( X_pr_T )

    L_pr = list()
    for k in K_pr:
       L_pr.append(l_pr[k])

    return (X_tr, Y_tr), (X_vl, Y_vl), (X_pr, L_pr)
