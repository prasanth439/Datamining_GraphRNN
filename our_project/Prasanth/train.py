from __future__ import absolute_import,division,print_function,unicode_literals
import tensorflow as tf 
from params import EPOCHS
'''
In tensorflow training
'''
def train():
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        init.run()
        for iters in range(EPOCHS):
            for batches in totalBatches:
                sess.run()
    return