# -*- coding: utf-8 -*-
"""Individiual_Pipeline.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-fe_mOlp4UK015tVJ3ovGK7njPjkYSFG
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from  tensorflow.keras import layers, Model
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


data_path= 'Multiclass Diabetes Dataset.csv'
df= pd.read_csv(data_path)

features= df.drop(columns=['Class'])
target= df['Class']

scaler=MinMaxScaler()

scaled_feat=scaler.fit_transform(features)





X_train, X_test, y_train, y_test= train_test_split(scaled_feat,target, test_size=.9,random_state=500)

https://www.tensorflow.org/tutorials/generative/autoencoder


class Autoencoder(Model):
  def __init__(self,latent_dim,shape):
      super(Autoencoder,self).__init__()
      self.latent_dim=latent_dim
      self.shape=shape
      self.encoder = tf.keras.Sequential([
          layers.Flatten(),
          layers.Dense(latent_dim,activation='selu')
      ])

      self.decoder= tf.keras.Sequential([
          layers.Dense(tf.math.reduce_prod(shape).numpy(),activation='sigmoid'),
          layers.Reshape(shape)
      ])

  def call(self,x):
    encoded= self.encoder(x)
    decoded=self.decoder(encoded)
    return decoded



shape= X_train.shape[1:]
latent_dim = 64


autoencoder = Autoencoder(latent_dim,shape)
autoencoder.compile(optimizer='adam', loss='mae')


history= autoencoder.fit(
  X_train, X_train,
  epochs=10,
  shuffle = True,
  validation_data= (X_test,X_test)

)



reconstructions= autoencoder.predict(X_test)
mse= np.mean(np.power(X_test- reconstructions, 2), axis=1)
threshold = np.percentile(mse, 95)

anamolies= mse > threshold


predictions = np.where (anamolies, 1, 0 )


accuracy_score= accuracy_score(y_test,predictions)
precision = precision_score (y_test, predictions, average='weighted' )
recall= recall_score(y_test, predictions,average= 'weighted')
f1=f1_score(y_test, predictions, average='weighted')



# output


print( "reconstruction score is :", threshold )
print( " anamolies  is :", np.sum(anamolies) )
print( "accuracy score is :", accuracy_score )
print( "precision  is :",  precision)
print( "recall  is :",  recall )
print( "f1 score is :",  f1)
