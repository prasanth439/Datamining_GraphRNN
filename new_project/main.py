import numpy as np
import sys
import os
from time import gmtime, strftime
from tensorboard_logger import configure

from graph_process import convert_to_networkGraphs
import random
from params import *
from helper import *


def debug(*args,**kwargs):
    print(*args,file=sys.stderr,**kwargs)


model_save_path = "/saved/model"
graph_save_path = "/saved/graph"
figure_save_path = "/saved/figure"
timing_save_path = "/saved/timing"
figure_prediction_save_path = "/saved/figure_prediction"
nll_save_path = "/saved/nll"

#  permission issue

# if not os.path.isdir(model_save_path):
#     os.makedirs(model_save_path)
# if not os.path.isdir(graph_save_path):
#     os.makedirs(graph_save_path)
# if not os.path.isdir(figure_save_path):
#     os.makedirs(figure_save_path)
# if not os.path.isdir(timing_save_path):
#     os.makedirs(timing_save_path)
# if not os.path.isdir(figure_prediction_save_path):
#     os.makedirs(figure_prediction_save_path)
# if not os.path.isdir(nll_save_path):
#     os.makedirs(nll_save_path)

time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

# logging.basicConfig(filename='logs/train' + time + '.log', level=logging.DEBUG)


# configure("tensorboard/run"+time, flush_secs=5)


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
graphValidation = nGraphList[:int(0.3*numGraphs)]
# debug("Training data")
# debug(graphTrain)


MAX_NODES = getMaxNodes(nGraphList)

# print('max number node: {}'.format(MAX_NODES))

# save_graph_list(nGraphList, graph_save_path + 'graphtrain.dat')
# save_graph_list(nGraphList, graph_save_path + 'graphtest.dat')
# print('train and test graphs saved at: ', graph_save_path + '.dat')

# change method name and param names
dataset = Graph_sequence_sampler_pytorch(graphTrain,max_prev_node=CONTEXT,max_num_node=MAX_NODES)
sample_strategy = torch.utils.data.sampler.WeightedRandomSampler([1.0 / len(dataset) for i in range(len(dataset))],
                                                                    num_samples=BATCH_SIZE*BATCH_RATIO, replacement=True)
dataset_loader = torch.utils.data.DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=NUM_WORKERS,
                                            sampler=sample_strategy)


#  train(dataset_loader, rnn, output)



'''
[1] Make history method 
[2] create batches 
[3] make RNN model (check dimensions)

'''

# adjacency matrices

