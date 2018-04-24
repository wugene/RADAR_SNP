
# coding: utf-8


import sys
import numpy as np
import pandas as pd
import _pickle as pkl
import gzip

import keras
from keras.models import Sequential, Model
from keras.layers.core import Dropout, Reshape, Flatten, Activation
from keras.layers.convolutional import MaxPooling2D, Conv2D

get_dataset = __import__('21_get_dataset')

if (len(sys.argv)<2):
    dataset_permut = 0
else:
    dataset_permut = int(sys.argv[1])

# Make datafiles
(X_tr, Y_tr), (X_vl, Y_vl), (X_pr, L_pr) = get_dataset.read_datafile(dataset_permut)

X_tr = np.expand_dims(X_tr, axis=3)
X_vl = np.expand_dims(X_vl, axis=3)
X_pr = np.expand_dims(X_pr, axis=3)

Y_tr = np.expand_dims(Y_tr, axis=1)
Y_vl = np.expand_dims(Y_vl, axis=1)


print ('Training set:', X_tr.shape, Y_tr.shape)
print ('Validataion set:', X_vl.shape, Y_vl.shape)

(n_sample, n_snp, n_feature, n_chan) = X_tr.shape
print ("n_sample =", n_sample, ", n_snp in image =", n_snp, ", n_feature in image =", n_feature)


# In[8]:
def make_model():

    model = Sequential()

    model.add(Conv2D(
        20, kernel_size=(1, n_feature), input_shape=(n_snp, n_feature, 1),
        activation='relu'
    ))
    model.add(Dropout(0.1))
    model.add(Reshape((n_snp,20,1)))

    model.add(Conv2D(
        100, kernel_size=(1, 20),
        activation='relu'
    ))
    model.add(Dropout(0.8))
    model.add(Reshape((n_snp,100,1)))

    model.add(Conv2D(
        20, kernel_size=(1, 100),
        activation='relu'
    ))
    model.add(Dropout(0.1))
    model.add(Reshape((n_snp,20,1)))

    model.add(Conv2D(
        1, kernel_size=(1, 20),
        activation='relu',
        name='snps'
    ))
    model.add(MaxPooling2D(pool_size=(n_snp,1)))

    model.add(Flatten())
    model.add(Activation(activation='relu'))

    model.summary()


    optimizer=keras.optimizers.Nadam(lr=0.0001)
    model.compile(
        loss='mean_squared_error', optimizer=optimizer,
        metrics=['acc']
    )
    return model


model = make_model()
earlystop = keras.callbacks.EarlyStopping()

history = model.fit(
    X_tr, Y_tr, batch_size=100, epochs=10,
    validation_data=(X_vl, Y_vl),
    callbacks = [earlystop]
)





pred_model = Model(inputs=model.input,
                  outputs=model.get_layer('snps').output)

pred_snp = pred_model.predict(X_pr)




# save prediction values
fn = 'PRED/predict.%d.tsv' % (dataset_permut)
with open(fn, 'w') as f:
  for i in zip(L_pr, pred_snp):
    preds = i[1].flatten()[0:len(i[0])]
    for k, v in zip(i[0], preds):
      print('%s\t%d\t%f' %(k[0], k[1], v), file=f)

print("Output complete: %s" % (fn))

