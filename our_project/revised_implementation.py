import numpy as np

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
