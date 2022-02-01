#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 15:44:25 2022

@author: kallil
"""

import numpy as np
import math


LLNASIZE=8
    
# run the network and return the temporal pattern of the graph nodes
def get_temporal_pattern(G,Brule,Srule, steps, nbSize=LLNASIZE):
    
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
            
            
    return x

#calculate shannon entropy of a time series x of a network
def shannon_entropy(x):
    s = 0
    for i in range(x.shape[1]):
        node_sum = 0
        for j in range(x.shape[0]):
            node_sum += x[j][i]
            
        prob_0 = node_sum/x.shape[0]
        prob_1 = 1-prob_0
        
        if(prob_0 >0 and prob_1 >0): 
            s -= (prob_0*math.log2(prob_0) + prob_1*math.log2(prob_1))
        elif(prob_0 > 0 and prob_1 <= 0):
            s -= prob_0*math.log2(prob_0)
        elif(prob_1 > 0 and prob_0 <=0):
            s -= prob_1*math.log2(prob_1)
    
    s /= x.shape[1]
    
    return s
    
#calculate word entropy of a time series x of a network
def word_entropy(x):
    w = 0
    
    for i in range(x.shape[1]):
        node_sum = 0
        word_size = 0
        freq = np.zeros(x.shape[0])
        for j in range(x.shape[0]):
            if(x[j][i] == 0):
                if(word_size != 0):
                    freq[word_size - 1] += 1
                    word_size = 0
            else:
                word_size +=1
            if(j == x.shape[0]-1):
                if(word_size != 0):
                    freq[word_size - 1] += 1
                    word_size = 0
        
        for j in range(x.shape[0]):
            if(freq[j] != 0):
                node_sum -= (freq[j]/np.sum(freq))*math.log2(freq[j]/np.sum(freq))
            
        w += node_sum
        
    
    return w / x.shape[1]
    
  
def lempel_ziv(x):
    
    lempel_ziv=0
    for i in range(x.shape[1]):
        u,v,w = 0,1,1
        v_max=1
        length = x.shape[0]
        complexity = 1
        while True:
            if(x[u+v-1,i] == x[w+v-1,i]):
                v+=1
                if(w+v >= length):
                    complexity+=1
                    break
            else:
                if(v>v_max):
                    v_max=v
                u += 1
                if u==w:
                    complexity+=1
                    w+=v_max
                    if(w>length):
                        break
                    else:
                        u=0
                        v=1
                        v_max=1
                else:
                    v=1
        lempel_ziv+=complexity*math.log2(length)/length
        
    return lempel_ziv/x.shape[1]