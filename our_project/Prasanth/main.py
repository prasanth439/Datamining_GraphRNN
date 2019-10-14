from __future__ import absolute_import,division,print_function,unicode_literals
import tensorflow as tf 
import numpy as np
import sys
import os


from graph_process import convert_to_networkGraphs
import random
from params import *


def debug(*args,**kwargs):
    print(*args,file=sys.stderr,**kwargs)


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

