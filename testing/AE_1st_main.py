
# coding: utf-8

# In[1]:


import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


import gzip, pickle

G_f_src = "AE1_in.pkl.gz"
G_f_tar = "AE1_out.pkl.gz"

def load_data(fn):
    with gzip.open(fn) as f:
        return pickle.load(f)
    
def save_data(d, fn):
    with gzip.open(fn, "w") as f:
        pickle.dump(d, f)


# In[3]:


(G_k, G_x, G_y) = load_data(G_f_src)

import copy, math
data_tr = copy.deepcopy(G_x)

np.random.shuffle(data_tr)
data_te = copy.deepcopy(data_tr[0:512])


# In[4]:


n = len(G_x)
num_input = len(G_x[0])
print ("dim = (%d, %d)" % (num_input, n))


# In[5]:


# Training Parameters
learn_rate = 0.002
num_epoch  = 25
batch_size = 64
num_batch  = int (n / batch_size)

# Network Parameters
num_hidden_1 = int(num_input * 2.1 / 3.1) # 1st layer num features
num_hidden_2 = int(num_input * 2.6 / 9.6) # 2nd layer num features (the latent dim)

print ("Nodes: %d -> %d -> %d" % (num_input,num_hidden_1,num_hidden_2))


# In[6]:


# tf Graph input (only pictures)
X = tf.placeholder("float", [None, num_input])

weights = {
    'encoder_h1': tf.Variable(tf.random_normal([num_input, num_hidden_1])),
    'encoder_h2': tf.Variable(tf.random_normal([num_hidden_1, num_hidden_2])),
    'decoder_h1': tf.Variable(tf.random_normal([num_hidden_2, num_hidden_1])),
    'decoder_h2': tf.Variable(tf.random_normal([num_hidden_1, num_input])),
}
biases = {
    'encoder_b1': tf.Variable(tf.random_normal([num_hidden_1])),
    'encoder_b2': tf.Variable(tf.random_normal([num_hidden_2])),
    'decoder_b1': tf.Variable(tf.random_normal([num_hidden_1])),
    'decoder_b2': tf.Variable(tf.random_normal([num_input])),
}

# Building the encoder
def normalize(x):
    x_norm = tf.nn.sigmoid(x)
    return x_norm

def encoder(x):
    # Encoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']),
                                   biases['encoder_b1']))
    # Encoder Hidden layer with sigmoid activation #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['encoder_h2']),
                                   biases['encoder_b2']))
    return layer_2


# Building the decoder
def decoder(x):
    # Decoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h1']),
                                   biases['decoder_b1']))
    # Decoder Hidden layer with sigmoid activation #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['decoder_h2']),
                                   biases['decoder_b2']))
    return layer_2

# Construct model
X_norm     = normalize(X)
encoder_op = encoder(X_norm)
decoder_op = decoder(encoder_op)

# Prediction
y_pred = decoder_op
# Targets (Labels) are the input data.
y_true = X_norm

# Define loss and optimizer, minimize the squared error
loss = tf.reduce_mean(tf.pow(y_true - y_pred, 2))
optimizer = tf.train.AdamOptimizer(learn_rate).minimize(loss)

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()


# In[7]:


# Start Training
# Start a new TF session
with tf.Session() as sess:
    
    # Run the initializer
    sess.run(init)
    after_l = list()

    epoch_loss = sess.run(loss, feed_dict={X: G_x})
    print('Starting Loss: %f' % (epoch_loss))
    
    # Training
    for epoch in range(1, num_epoch+1):
        
        np.random.shuffle(data_tr)
        
        for i in range(num_batch):
            batch_x = data_tr[i*batch_size:(i+1)*batch_size]
           
            # Run optimization op (backprop) and cost op (to get loss value)
            _, l = sess.run([optimizer, loss], feed_dict={X: batch_x})
            
            steps = (epoch-1) * num_batch + i
            #if (int(math.sqrt(epoch))**2 == epoch) or (epoch == num_epoch):
            if (((int(math.sqrt(steps / 100.0))**2)*100)==steps):
                before, after, l = sess.run([X_norm, decoder_op, loss], feed_dict={X: data_te})
                print('Epoch %i: Testing Loss: %f' % (epoch, l))
                after_l.append(after)

        print('Epoch %i: Minibatch Loss: %f' % (epoch, l))

    G_x_enc, epoch_loss = sess.run([encoder_op, loss], feed_dict={X: G_x})
    print('Final Loss: %f' % (epoch_loss))


# In[8]:


n_after = 10 #len(after_l)
fig = plt.figure(figsize=(n_after+4,20), dpi=100)
for i in range(n_after):
    a = fig.add_subplot(1, n_after+1, i+1)
    plt.imshow(after_l[i][:24].T, origin="upper", cmap="bwr")
    plt.axis('off')

a = fig.add_subplot(1, n_after+1, n_after+1)
plt.imshow(before[:24].T, origin="upper", cmap="bwr")
plt.axis('on')
plt.show()


# In[9]:


plt.figure(figsize=(10,3), dpi=100)
plt.imshow(G_x_enc[:160000].T.reshape(800,-1), origin="upper", cmap="bwr")
plt.show()


# In[14]:


from scipy import stats

def normalize_enc(enc):
    enc_T = np.transpose(enc)
    enc_T_new = list()
    
    for T in enc_T:
        T_new = stats.zscore(T)
        for i in range(len(T_new)):
            if (T_new[i] > 5.0):
                T_new[i] = 5.0
            elif (T_new[i] < -5.0):
                T_new[i] = -5.0
                
        T_new_sum = sum(T_new)
        #print(T_new_sum)
        if (T_new_sum < 1.0) and (T_new_sum > -1.0):
            enc_T_new.append(T_new)
            
    return np.transpose(enc_T_new)


# In[15]:


G_x_norm = normalize_enc(G_x_enc)
print ("Normalization dim = (%d, %d) -> (%d, %d)" % (len(G_x_enc), len(G_x_enc[0]), len(G_x_norm), len(G_x_norm[0])))


# In[16]:


G_data_ae2 = (G_k, G_x_norm, G_y)
save_data(G_data_ae2, G_f_tar)


# In[17]:


plt.figure(figsize=(10,3), dpi=100)
plt.imshow(G_x_norm[:160000].T.reshape(800,-1), origin="upper", cmap="bwr")
plt.show()

