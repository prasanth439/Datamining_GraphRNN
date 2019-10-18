import argparse
import numpy as np
import os
import re
from random import shuffle

import eval.stats
import utils
# import main.Args


def load_ground_truth(dir_input, dataset_name, model_name='GraphRNN_RNN'):
    ''' Read ground truth graphs.
    '''
    if not 'small' in dataset_name:
        hidden = 128
    else:
        hidden = 64
   
    fname_test = dir_input + model_name + '_' + dataset_name + '_' + str(args.num_layers) + '_' + str(
            hidden) + '_test_' + str(0) + '.dat'
    try:
        graph_test = utils.load_graph_list(fname_test,is_real=True)
    except:
        print('Not found: ' + fname_test)
        logging.warning('Not found: ' + fname_test)
        return None
    return graph_test

def eval_single_list(graphs, dir_input, dataset_name):
    ''' Evaluate a list of graphs by comparing with graphs in directory dir_input.
    Args:
        dir_input: directory where ground truth graph list is stored
        dataset_name: name of the dataset (ground truth)
    '''
    graph_test = load_ground_truth(dir_input, dataset_name)
    graph_test_len = len(graph_test)
    graph_test = graph_test[int(0.8 * graph_test_len):] # test on a hold out test set
    mmd_degree = eval.stats.degree_stats(graph_test, graphs)
    mmd_clustering = eval.stats.clustering_stats(graph_test, graphs)
    try:
        mmd_4orbits = eval.stats.orbit_stats_all(graph_test, graphs)
    except:
        mmd_4orbits = -1
    print('deg: ', mmd_degree)
    print('clustering: ', mmd_clustering)
    print('orbits: ', mmd_4orbits)



if __name__ == '__main__':
    args = Args()
    graphs = utils.load_graph_list(prog_args.test_file)
    graphs = graphs[:len(graphs)/10]
    eval_single_list(graphs, dir_input=dir_prefix+'graphs/', dataset_name='protein')



