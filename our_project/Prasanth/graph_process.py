from __future__ import absolute_import,division,print_function,unicode_literals
import networkx as nx
import numpy as np
import tensorflow as tf 
from helper import *
import random
from params import HISTORY_ITERATIONS,MAX_NODES,HISTORY

'''
graph : network graph
return : list of nodes traversed in bfs
'''
def get_bfs_seq(graph):
  bfs_seq = []
  return bfs_seq


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
def makeRNN_IO(adjMatrices):
  io_list = []
  for adj_ in adjMatrices:
    data_x = np.zeros(MAX_NODES,HISTORY)
    data_y = np.zeros(MAX_NODES,HISTORY)
    data_len = len(adj_)

  return io_list

def makeBatches():
  


