#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 18:14:33 2022

@author: kallil
"""

import cv2
import numpy as np
import networkx as nx
import networklib as nl 
import llna 
import llnabp as lbp
import image_cn_modeling as icm
import os
import itertools


LLNASIZE=8
steps = 350
DATADIR = "data/USPTex/images/"

images_pathlist = [image for image in os.listdir(DATADIR)]

y=[]

for image_path in images_pathlist:
    y.append(int(image_path[1:4]))
    
    
#possible LLNA rules
values = []
bRules = []
sRules = []
for i in range(LLNASIZE+1):
    values.append(i)
    
for L in range(1, len(values)+1):
    for subset in itertools.combinations(values,L):
        bRules.append(subset)
        sRules.append(subset)

Graph_list = []
counter=1


for image_path in images_pathlist:
    print(f"Starting image {counter} of {len(images_pathlist)}\n")
    
    img = cv2.imread(DATADIR+image_path, cv2.IMREAD_GRAYSCALE)
    img_height, img_width = img.shape
    
    init_cond = np.random.randint(2,size=img_height*img_width)
    
    G = (icm.create_graph(img))
    
    nl.set_attributes(G, init_cond)
    
    icm.connect_neighborhood(img, G, R=1)
    
    for bRule in bRules:
        for sRule in sRules:
            
            print(f"{bRule}/{sRule}\n")
            
            lbp.get_temporal_pattern(G, bRule, sRule, steps)
            
            
            
    counter +=1