#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 19:28:45 2022

@author: kallil
"""

import cv2
import os
import networkx as nx
from scipy.spatial import distance
import numpy as np




R = 4
L = 255
def create_graph(img):
    img_height, img_width = img.shape
    G = nx.DiGraph()
    for i in range(img_height):
        for j in range(img_width):
            G.add_node((i,j))
            
    return G
    

#R is radius of connection and L is the maximum intensity of a pixel
def connect_neighborhood(img, G, R, L):
    img_height, img_width = img.shape

    
    for i in range(img_height):
        for j in range(img_width):
            for y in range(i-R, i+R+1):
                if(y>=0 and y<img_height):
                    for x in range(j-R,j+R+1):
                        if(x>=0 and x<img_width):
                            d = distance.euclidean((i,j),(y,x))
                            if(img[i,j]<img[y,x] and d<=R):
                                if(R==1):
                                    weight = (abs(img[i,j]-img[y,x])/L)
                                else:
                                    weight = ((d-1)/(R-1) + (abs(img[i,j]-img[y,x]))/L)/2
                                G.add_edge((i,j), (y,x), weight=weight)
    
            
    return G