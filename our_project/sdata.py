import networkx as nx
import numpy as np

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
