# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 16:49:06 2021

@author: kalli
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

#set graph initial conditions as node value attribute
#also, set node degree and node density
def set_attributes(G, init_cond):
    
    
    density = np.zeros(len(G.nodes))
    
    degree = np.zeros(len(G.nodes))
    
    
    
    for i,j in G.edges():
        degree[i]+=1
        degree[j]+=1
    
    for i,j in G.edges():
        if(init_cond[i]):
            density[j]+=1/degree[j]
        if(init_cond[j]):
            density[i]+=1/degree[i]
        
    attr = {0: {'value': init_cond[0],'density': density[0], 'degree': degree[0]}}
    
    for i in range(1,len(G.nodes)):
        attr[i] = {}
        attr[i]['value'] = init_cond[i]
        attr[i]['density'] = density[i]
        attr[i]['degree'] = degree[i]
        
    nx.set_node_attributes(G, attr)

#construct a regular network 
#with each node connected to his 4 closest neighbors
def create_regular(n=100):
    G = nx.Graph()
    
    for i in range(n):
        G.add_node(i)
        
    for i in range(n):
        if(i+1 >= n):
            G.add_edge(i, i+1-n)
        else:
            G.add_edge(i,i+1)
        if(i+2 >= n):
            G.add_edge(i, i+2-n)
        else:
            G.add_edge(i,i+2) 
    
    return G



#transform the regular network in a random network by 
# watts & Strogatz model using different p values
def reg2rand(G, p):
    
    n = len(G.nodes())
    
    for i in G.edges():
        r = np.random.uniform(0,1)
        if(r < p):
            G.remove_edge(i[0],i[1])
            v = np.random.randint(0,n)
            while(v == i[0]):
                v = np.random.randint(0,n)
            G.add_edge(i[0],v)
        
    return G

#calculate the mean of the clustering coefficient for each
#node in the graph
def mean_cc(G):
    values = []
    for i in range(len(G.nodes())):
        values.append(nx.clustering(G,i))
        
    values = np.array(values)
    
    return np.mean(values)

#calculate the average shortest path
def avg_path(G):
    
    if(nx.is_connected(G)):
        return nx.average_shortest_path_length(G)
    else:
        paths=[]
        for i in range(len(G.nodes)):
            for j in range(i+1, len(G.nodes)):
                if(nx.has_path(G,i,j)): 
                    paths.append(len(nx.shortest_path(G,i,j))-1)
        paths = np.array(paths)
        return np.mean(paths)
    