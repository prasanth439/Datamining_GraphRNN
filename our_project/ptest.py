import networkx as nx 
import numpy as np
from sdata import convert_to_networkGraphs
def bfs_seq(G, start_id):
    '''
    get a bfs node sequence
    :param G:
    :param start_id:
    :return:
    '''
    dictionary = dict(nx.bfs_successors(G, start_id))
    start = [start_id]
    output = [start_id]
    while len(start) > 0:
        next = []
        while len(start) > 0:
            current = start.pop(0)
            neighbor = dictionary.get(current)
            if neighbor is not None:
                #### a wrong example, should not permute here!
                # shuffle(neighbor)
                next = next + neighbor
        output = output + next
        start = next
    return output

def encode_adj_flexible(adj):
    '''
    return a flexible length of output
    note that here there is no loss when encoding/decoding an adj matrix
    :param adj: adj matrix
    :return:
    '''
    # pick up lower tri
    adj = np.tril(adj, k=-1)
    n = adj.shape[0]
    adj = adj[1:n, 0:n-1]
    print(adj)
    adj_output = []
    input_start = 0
    for i in range(adj.shape[0]):
        input_end = i + 1
        adj_slice = adj[i, input_start:input_end]
        adj_output.append(adj_slice)
        non_zero = np.nonzero(adj_slice)[0]
        input_start = input_end-len(adj_slice)+np.amin(non_zero)
    return adj_output

def encode_adj(adj, max_prev_node=10, is_full = False):
    '''

    :param adj: n*n, rows means time step, while columns are input dimension
    :param max_degree: we want to keep row number, but truncate column numbers
    :return:
    '''
    if is_full:
        max_prev_node = adj.shape[0]-1

    # pick up lower tri
    adj = np.tril(adj, k=-1)
    n = adj.shape[0]
    adj = adj[1:n, 0:n-1]

    # use max_prev_node to truncate
    # note: now adj is a (n-1)*(n-1) matrix
    adj_output = np.zeros((adj.shape[0], max_prev_node))
    for i in range(adj.shape[0]):
        input_start = max(0, i - max_prev_node + 1)
        input_end = i + 1
        output_start = max_prev_node + input_start - input_end
        output_end = max_prev_node
        adj_output[i, output_start:output_end] = adj[i, input_start:input_end]
        adj_output[i,:] = adj_output[i,:][::-1] # reverse order

    return adj_output


data_file = "test_data.txt"
gGraphs = convert_to_networkGraphs(data_file=data_file)
print("Graph 1 details")
print(nx.get_node_attributes(gGraphs[1],'label'))
print(gGraphs[1].edges())
print(gGraphs[1].nodes())
# print("Graph 0 details")
# print(nx.get_node_attributes(gGraphs[0],'label'))
# print(gGraphs[0].edges())
# G = None
m = (np.asarray(nx.to_numpy_matrix(gGraphs[1])))
# G = nx.from_numpy_matrix(y)
# print(G.nodes())
m = np.asarray([[0,0,0,0,0],[1,0,0,0,0],[0,1,0,0,0],[0,1,0,0,0],[1,0,0,0,0]])
m=m.T+m
G = nx.from_numpy_matrix(m)
            # then do bfs in the permuted G
start_idx = np.random.randint(m.shape[0])
x_idx = np.array(bfs_seq(G, start_idx))
m = m[np.ix_(x_idx, x_idx)]
# encode adj
adj_encoded = encode_adj(m.copy())
print(adj_encoded)
# print(np.asarray(nx.to_numpy_matrix(gGraphs[1])))
