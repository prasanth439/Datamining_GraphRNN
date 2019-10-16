import numpy as np
import networkx as nx

from helper import *
import random
from params import *

'''
graph : network graph
return : list of nodes traversed in bfs
'''

def bfs_seq(Graphset_complete, initial_node_id):

    dict_nodewise_bfs_seq = nx.bfs_successors(Graphset_complete, initial_node_id)
    initial_nodes = [initial_node_id]
    output = [initial_node_id]

    # code for generating BFS sequence of a given graph
    while len(initial_nodes) > 0:
        current = initial_nodes.pop(0)
        siblings = dict_nodewise_bfs_seq.get(current)
        if siblings is not None:
          initial_nodes = initial_nodes + siblings
          output = output + siblings

    # code given in the data.py
    # while len(initial_nodes) > 0:
    #     nextnodes = []
    #     while len(initial_nodes) > 0:
    #         current = initial_nodes.pop(0)
    #         siblings =  dict_nodewise_bfs_seq.get(current)
    #         if siblings is not None:
    #             nextnodes = nextnodes + siblings
    #     output = output + nextnodes
    #     initial_nodes = initial_nodes + nextnodes

    return output


# This method will return an encoded output adjacency matrix
# is_full is always null so no need to worry about is_full scenario
# Pick lower traingle, diagonal element k=-1, np.tril method
# n as number of rows/time steps
# Take 1...N and 0 to N-1
# adj_output =  Take segment of matrix (n-1)*(n-1) matrix
# np.zeros((adj.shape[0], max_prev_node))
# Adj_output: Initialize it to zeroes
# i in 0 to row - 1

def encode_adj(adj, max_prev_node=10):

    # pick up lower triangle
    # Diagonal above which to zero elements.
    # k = 0 (the default) is the main diagonal, k < 0 is below it and k > 0 is above.
    adj_lower_triangle = np.tril(adj, k=-1)
    num_row = adj.shape[0]
    adj_lower_triangle = adj_lower_triangle[1:num_row, 0:num_row-1]

    # For a adjacency matrix
    # [[0. 1. 1. 0. 0.]
    # [1. 0. 1. 1. 0.]
    # [1. 1. 0. 0. 1.]
    # [0. 1. 0. 0. 0.]
    # [0. 0. 1. 0. 0.]]

    #Lower Triangle will be
    # [[1. 0. 0. 0.]
    #  [1. 1. 0. 0.]
    #  [0. 1. 0. 0.]
    # [0. 0. 1. 0.]]

    # Final output is
    # [[1. 0. 0.]
    #  [1. 1. 0.]
    #  [0. 1. 0.]
    #  [0. 1. 0.]]

    # use max_prev_node to truncate
    # note: now adj is a (n-1)*(n-1) matrix
    adj_encoded_output = np.zeros((num_row-1, max_prev_node))
    for i in range(num_row-1):
        # Look back till max_prev_node from the node position
        input_start = max(0, i - max_prev_node + 1)
        # Look forward till diagonal element
        input_end = i + 1
        # starting point of output
        output_start = max_prev_node + input_start - input_end
        # size of context array
        output_end = max_prev_node
        adj_encoded_output[i, output_start:output_end] = adj_lower_triangle[i, input_start:input_end]
        # Reversal as this will go as input to the next stage
        adj_encoded_output[i,:] = adj_encoded_output[i,:][::-1] # reverse order

    return adj_encoded_output

# This method can be combined with the encode_adj method
# Just pass the flexible flag at this point
def encode_adj_flexible(adj):
    '''
    return a flexible length of output
    note that here there is no loss when encoding/decoding an adj matrix
    :param adj: adj matrix
    :return:
    '''
    # pick up lower tri
    adj_lower_triangle = np.tril(adj, k=-1)
    num_row = adj.shape[0]
    adj_lower_triangle = adj_lower_triangle[1:num_row, 0:num_row - 1]

    adj_ecoded_output = []
    input_start = 0
    for i in range(adj.shape[0]):
        input_end = i + 1
        adj_slice = adj_lower_triangle[i, input_start:input_end]
        adj_ecoded_output.append(adj_slice)
        non_zero = np.nonzero(adj_slice)[0]
        input_start = input_end-len(adj_slice)+np.amin(non_zero)

    return adj_ecoded_output


'''
we need to change decode 
'''

# def decode_adj(adj_output):
#     '''
#         recover to adj from adj_output
#         note: here adj_output have shape (n-1)*m
#     '''
#     max_prev_node = adj_output.shape[1]
#     adj = np.zeros((adj_output.shape[0], adj_output.shape[0]))
#     for i in range(adj_output.shape[0]):
#         input_start = max(0, i - max_prev_node + 1)
#         input_end = i + 1
#         output_start = max_prev_node + max(0, i - max_prev_node + 1) - (i + 1)
#         output_end = max_prev_node
#         adj[i, input_start:input_end] = adj_output[i,::-1][output_start:output_end] # reverse order
#     adj_full = np.zeros((adj_output.shape[0]+1, adj_output.shape[0]+1))
#     n = adj_full.shape[0]
#     adj_full[1:n, 0:n-1] = np.tril(adj, 0)
#     adj_full = adj_full + adj_full.T

#     return adj_full



# def decode_adj_flexible(adj_output):
#     '''
#     return a flexible length of output
#     note that here there is no loss when encoding/decoding an adj matrix
#     :param adj: adj matrix
#     :return:
#     '''
#     adj = np.zeros((len(adj_output), len(adj_output)))
#     for i in range(len(adj_output)):
#         output_start = i+1-len(adj_output[i])
#         output_end = i+1
#         adj[i, output_start:output_end] = adj_output[i]
#     adj_full = np.zeros((len(adj_output)+1, len(adj_output)+1))
#     n = adj_full.shape[0]
#     adj_full[1:n, 0:n-1] = np.tril(adj, 0)
#     adj_full = adj_full + adj_full.T

#     return adj_full


'''
Dont know the usage
'''
# def test_encode_decode_adj():
# ######## code test ###########
#     G = nx.ladder_graph(5)
#     G = nx.grid_2d_graph(20,20)
#     G = nx.ladder_graph(200)
#     G = nx.karate_club_graph()
#     G = nx.connected_caveman_graph(2,3)
#     print(G.number_of_nodes())
    
#     adj = np.asarray(nx.to_numpy_matrix(G))
#     G = nx.from_numpy_matrix(adj)
#     #
#     start_idx = np.random.randint(adj.shape[0])
#     x_idx = np.array(bfs_seq(G, start_idx))
#     adj = adj[np.ix_(x_idx, x_idx)]
    
#     print('adj\n',adj)
#     adj_output = encode_adj(adj,max_prev_node=5)
#     print('adj_output\n',adj_output)
#     adj_recover = decode_adj(adj_output,max_prev_node=5)
#     print('adj_recover\n',adj_recover)
#     print('error\n',np.amin(adj_recover-adj),np.amax(adj_recover-adj))
    
    
#     adj_output = encode_adj_flexible(adj)
#     for i in range(len(adj_output)):
#         print(len(adj_output[i]))
#     adj_recover = decode_adj_flexible(adj_output)
#     print(adj_recover)
#     print(np.amin(adj_recover-adj),np.amax(adj_recover-adj))

# def decode_adj_full(adj_output):
#     '''
#     return an adj according to adj_output
#     :param
#     :return:
#     '''
#     # pick up lower tri
#     adj = np.zeros((adj_output.shape[0]+1,adj_output.shape[1]+1))

#     for i in range(adj_output.shape[0]):
#         non_zero = np.nonzero(adj_output[i,:,1])[0] # get valid sequence
#         input_end = np.amax(non_zero)
#         adj_slice = adj_output[i, 0:input_end+1, 0] # get adj slice
#         # write adj
#         output_end = i+1
#         output_start = i+1-input_end-1
#         adj[i+1,output_start:output_end] = adj_slice[::-1] # put in reverse order
#     adj = adj + adj.T
#     return adj

# def test_encode_decode_adj_full():
# ########### code test #############
#     # G = nx.ladder_graph(10)
#     G = nx.karate_club_graph()
#     # get bfs adj
#     adj = np.asarray(nx.to_numpy_matrix(G))
#     G = nx.from_numpy_matrix(adj)
#     start_idx = np.random.randint(adj.shape[0])
#     x_idx = np.array(bfs_seq(G, start_idx))
#     adj = adj[np.ix_(x_idx, x_idx)]
    
#     adj_output, adj_len = encode_adj_full(adj)
#     print('adj\n',adj)
#     print('adj_output[0]\n',adj_output[:,:,0])
#     print('adj_output[1]\n',adj_output[:,:,1])
#     # print('adj_len\n',adj_len)
    
#     adj_recover = decode_adj_full(adj_output)
#     print('adj_recover\n', adj_recover)
#     print('error\n',adj_recover-adj)
#     print('error_sum\n',np.amax(adj_recover-adj), np.amin(adj_recover-adj))



'''
datafile : string of file name
returns : graph list
'''
def convert_to_networkGraphs(data_file=None):
    if(data_file==None):
      print("No given datafile")
      exit()
		
    graphstable = []
    total_node = 0
    total_edge = 0
    total_graph = 0

    node_label_map = {}
    data_node_label = []
    nodelabelcount = 1
    graphs = []
    data_graph_labels = []
    nodelist_graph = []
    edgelist_graph = []
    num_node = 0
    num_edge = 0
    flag = 1
    f = open(data_file, "r")
    while True:
      line = f.readline()
      if line == '':
        break
      G = nx.Graph() 
      # print(line)
      # continue
      id_line = "#" in line
      if (id_line):
        data_graph_labels.insert(total_graph, 1)
        total_graph = total_graph + 1
        nodelist_graph = []
        edgelist_graph = []
        # reset nodelist_graph and edgelist_graph
        if (flag == 1):
          graph = {}
        else:
          flag = 0

        num_node = 0
        num_edge = 0
        # Reset all the variables

        num_node = int(f.readline(), 10)
        for x in range(num_node):
          node_iter = f.readline()
          node_flag = node_label_map.get(node_iter)
          if node_flag is None:
            node_label_map[node_iter]  = nodelabelcount
            nodelabelcount = nodelabelcount + 1
          # adding vertex to node_list
          # nodelist_graph.insert(x, node_label_map.get(node_iter))
          nodelist_graph.append(node_label_map.get(node_iter))

        num_edge = int(f.readline())

        for x in range (num_edge):
          edge_iter = f.readline().split()
          # edge = [int(edge_iter[0]) + 1 , int(edge_iter[1]) + 1 ]
          edge = [int(edge_iter[0]) + 1 + total_node, int(edge_iter[1]) + 1 + total_node]
          edgelist_graph.insert(x, edge)
          # edgelist_graph.insert(x, edge)


        graph["num_node"] = num_node
        graph["num_edge"] = num_edge
        graph["nodelist"] = nodelist_graph
        graph["edgelist"] = edgelist_graph
        graphstable.append(graph)
        print(graph)
        #sys.exit()
        edgelist_graph_tuple = list(map(tuple,edgelist_graph))
        G.add_edges_from(edgelist_graph_tuple)
        for i in range(len(nodelist_graph)):
          G.add_node(total_node+i+1, label = nodelist_graph[i])
        G.remove_nodes_from(list(nx.isolates(G)))
        total_edge = total_edge + num_edge
        total_node = total_node + num_node
        graphs.append(G)
    #graphstablemap.append(G_sub)

    #return graphstablemap


    
    return graphs

'''
params : network graphs
returns : adjacency matrices from network graphs
'''
def getAdjMatList(graphList):
  adj_list = []
  for g in graphList:
    adj_list.append(getAdjMatNormal(g))
  return adj_list



########## use pytorch dataloader
class Graph_sequence_sampler_pytorch(torch.utils.data.Dataset):
    def __init__(self, G_list, max_num_node=None, max_prev_node=None, iteration=20000):
        self.adj_all = []
        self.len_all = []
        for G in G_list:
            self.adj_all.append(np.asarray(nx.to_numpy_matrix(G)))
            self.len_all.append(G.number_of_nodes())
        if max_num_node is None:
            self.n = max(self.len_all)
        else:
            self.n = max_num_node
        if max_prev_node is None:
            print('calculating max previous node, total iteration: {}'.format(iteration))
            self.max_prev_node = max(self.calc_max_prev_node(iter=iteration))
            print('max previous node: {}'.format(self.max_prev_node))
        else:
            self.max_prev_node = max_prev_node

        # self.max_prev_node = max_prev_node
        # # sort Graph in descending order
        # len_batch_order = np.argsort(np.array(self.len_all))[::-1]
        # self.len_all = [self.len_all[i] for i in len_batch_order]
        # self.adj_all = [self.adj_all[i] for i in len_batch_order]
    def __len__(self):
        return len(self.adj_all)
    def __getitem__(self, idx):
        adj_copy = self.adj_all[idx].copy()
        x_batch = np.zeros((self.n, self.max_prev_node))  # here zeros are padded for small graph
        x_batch[0,:] = 1 # the first input token is all ones
        y_batch = np.zeros((self.n, self.max_prev_node))  # here zeros are padded for small graph
        # generate input x, y pairs
        len_batch = adj_copy.shape[0]
        x_idx = np.random.permutation(adj_copy.shape[0])
        adj_copy = adj_copy[np.ix_(x_idx, x_idx)]
        adj_copy_matrix = np.asmatrix(adj_copy)
        G = nx.from_numpy_matrix(adj_copy_matrix)
        # then do bfs in the permuted G
        start_idx = np.random.randint(adj_copy.shape[0])
        x_idx = np.array(bfs_seq(G, start_idx))
        adj_copy = adj_copy[np.ix_(x_idx, x_idx)]
        adj_encoded = encode_adj(adj_copy.copy(), max_prev_node=self.max_prev_node)
        # get x and y and adj
        # for small graph the rest are zero padded
        y_batch[0:adj_encoded.shape[0], :] = adj_encoded
        x_batch[1:adj_encoded.shape[0] + 1, :] = adj_encoded
        return {'x':x_batch,'y':y_batch, 'len':len_batch}


'''
params : adjMatrices
returns : maxHistory
'''
def calculateHistory(adjMatrices):
  history = 0
  numMatrices = len(adjMatrices) #number of matrices
  for iter in range(HISTORY_ITERATIONS):
    mat_id = random.randint(0,numMatrices)
    adj_dup = adjMatrices[mat_id].copy()
    node_indexes = [i for i in range(len(adj_dup))]
    per_node_indexes = np.random.permutation(node_indexes) # permuted node indexex
    adj_dup = adj_dup[np.ix_(per_node_indexes,per_node_indexes)]
    node_index = random.randint(0,len(adj_dup))
    G = nx.from_np(adj_dup)
    bfs_seq = get_bfs_seq(G,node_index)
    adj_dup = adj_dup[np.ix_(bfs_seq,bfs_seq)]
    encoded_matrix = get_encode_variable(adj_dup.copy())
    local_history = max([len(row) for row in encoded_matrix])
    history = max(history,local_history)
  return history
'''
params : adjMatrices
returns : input output pairs of graphs
'''


