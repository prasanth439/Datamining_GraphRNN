from __future__ import absolute_import,division,print_function,unicode_literals
import tensorflow as tf 
from params import EPOCHS,TEST_EPOCHS
from helper import debug
'''
In tensorflow training
'''
def train(batches,modelA,modelB):
    for epocNo in range(EPOCHS):





        if epocNo%TEST_EPOCHS ==0 and epocNo >= TEST_START:
            debug("Test not done")
            pass
    return