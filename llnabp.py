# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 13:58:46 2021

@author: kalli
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import watts_strogatz as ws
import itertools
import math
import pandas as pd
import seaborn as sns


LLNASIZE=8

  
#encode the decimal binary patterns of the TEP
def dec_bp(data, d):
    """
    Parameters
    ----------
    data : temporal evolution pattern numpy array.
    d : number of bits.

    Returns
    -------
    phi_d: decimal format of the binary pattern.
    
    """
    phi_d = np.zeros((data.shape[0]-d+1,data.shape[1]))
    
    for i in range(phi_d.shape[1]):
        for j in range(phi_d.shape[0]):
            for k in range(j,(d)+j):
                phi_d[j,i] += data[k,i]*2**(k-j)
                    
    return phi_d
              

#compute the global histogram of the binary patterns
def global_hist(phi_d,d):
    
    p_max = 2**d-1
    
    
    H_g = np.zeros(p_max+1)
    
    for i in range(phi_d.shape[1]):
        for j in range(phi_d.shape[0]):
            for p in range(p_max+1):
                if(phi_d[j,i] == p):
                    H_g[p] +=1
                
                    
              
    return H_g/np.sum(H_g)

#compute the degree histogram of the binary patterns
def degree_hist(G, phi_d,d, k):
    
    p_max = 2**d-1
    
    
    H_k = np.zeros(p_max+1)
    
    for i in range(phi_d.shape[1]):
        if(G.degree[i] ==k):
            for j in range(phi_d.shape[0]):
                for p in range(p_max+1):
                    if(phi_d[j,i] == p):
                        H_k[p] +=1
                
                    
    if(np.sum(H_k)==0):
        return H_k
    return H_k/np.sum(H_k)

def hist_to_dec(H):
    dec = 0
    for i in range(len(H)):
        dec+= H[i]*(2**i)
    
    return dec/2**(len(H)-1)
  

# run the network and return the temporal pattern of the graph nodes
def get_temporal_pattern(G,Brule,Srule, steps, nbSize=LLNASIZE):
    
    discard = steps//4
    
    x = np.zeros((steps, len(G.nodes)))
    
    for i in range(len(G.nodes)):
        x[0][i] = G.nodes[i]['value']
    
    for i in range(1,steps):    
        for j in range(len(G.nodes)):
            if(G.nodes[j]['value'] == 0):
                total = 0
                for k in Brule:
                    
                    density = G.nodes[j]['density']
                    if(k < nbSize and (k/(nbSize+1) <= density and density < k+1/(nbSize+1))):
                        total+=1
                        break
                    elif(k == nbSize and (k/(nbSize+1) <= density and density <= k+1/(nbSize+1))):
                        total+=1
                        break
                if(total > 0):
                    G.nodes[j]['value']=1
                else:
                    G.nodes[j]['value']=0
            else:
                total = 0
                for k in Srule:
                    
                    density = G.nodes[j]['density']
                    if(k < nbSize and (k/(nbSize+1) <= density and density < k+1/(nbSize+1))):
                        total+=1
                        break
                    elif(k == nbSize and (k/(nbSize+1) <= density and density <= k+1/(nbSize+1))):
                        total+=1
                        break
                if(total > 0):
                    G.nodes[j]['value']=1
                else:
                    G.nodes[j]['value']=0
            
            x[i][j] = G.nodes[j]['value']
        
        density = np.zeros(len(G.nodes))
        for k,l in G.edges():
            if(x[i][k]):
                density[l]+=1/G.nodes[l]['degree']
            if(x[i][l]):
                density[k]+=1/G.nodes[k]['degree']
                
        for k in range(len(G.nodes)):
            G.nodes[k]['density'] = density[k]
            
            
    return x[discard:,]

