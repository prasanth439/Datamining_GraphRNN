from __future__ import absolute_import,division,print_function,unicode_literals
import tensorflow as tf 
import numpy as np


'''
params : unknown
returns : RNN Model
'''
def makeRNN_model(input_size, embedding_size, hidden_size, num_layers):
    tf.keras.layers.Dense(embedding_size,input_shape=(input_size,)

    return model