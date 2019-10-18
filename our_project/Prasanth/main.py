from __future__ import absolute_import,division,print_function,unicode_literals
import tensorflow as tf 
import numpy as np
import sys
import os


from graph_process import convert_to_networkGraphs
import random
from params import *
from helper import *
from train import *
tf.enable_eager_execution()



input_file = sys.argv[1]
debug("Reading input file %s" % input_file) 

nGraphList = convert_to_networkGraphs(input_file)
print(nGraphList)
numGraphs = len(nGraphList)
debug("Total number of graphs %d" % numGraphs)

random.seed(200)
random.shuffle(nGraphList)
graphTest = nGraphList[int(0.7*numGraphs):]
graphTrain = nGraphList[:int(0.7*numGraphs)]

debug("Training data")
debug(graphTrain)


'''
[1] Make history method 
[2] create batches 
[3] make RNN model (check dimensions)
'''

# adjacency matrices
MAX_NODES = getMaxNodes(nGraphList)

all_adj_matrices = getAdjMatList(graphTrain[:len(graphTrain)-len(graphTrain)%BATCH_SIZE])
X,Y,len_list= makeRNN_IO(all_adj_matrices)
tf_data1 = tf.data.Dataset.from_tensor_slices(np.array(X))
tf_data2 = tf.data.Dataset.from_tensor_slices(np.array(Y))
tf_data3 = tf.data.Dataset.from_tensor_slices(np.array(len_list))
tf_data4 = tf.data.Dataset.zip((tf_data1,tf_data2,tf_data3)).shuffle(5).batch(BATCH_SIZE)

modelA = makeRNN_model()
modelB = makeRNN_model()

train(tf_data4,modelA,modelB)


