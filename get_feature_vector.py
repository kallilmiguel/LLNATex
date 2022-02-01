#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 17:28:35 2022

@author: kallil
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from neural_network_model import RNN
import cv2
import os
import networkx as nx
from scipy.spatial import distance
import image_cn_modeling as icm

def get_from_dataset():
    dataset=pd.read_csv('50_Startups.csv')
    X = dataset.iloc[:,:-1].values
    y = dataset.iloc[:, -1].values
    
    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [3])], 
                           remainder='passthrough')
    X = np.array(ct.fit_transform(X),dtype=np.float64)
    
    
    rows = X.shape[0]
    columns = X.shape[1]
    
    
    return X,y,rows,columns

def get_cn_measures(G):
    #array to store out degree values
    x_out = np.zeros(shape=len(G.nodes))
    #array to store weighted out degree values
    x_wout = np.zeros(shape=len(G.nodes))
    #array to store weighted in degree values
    x_win = np.zeros(shape=len(G.nodes))
    
    for i in range(len(G.nodes)):
        x_out[i] = G.out_degree(list(G.nodes)[i])
        x_wout[i] = G.out_degree(list(G.nodes)[i], weight='weight')
        x_win[i] = G.in_degree(list(G.nodes)[i], weight='weight')    
    
    return x_out, x_wout, x_win


def get_labels_from_image(img):
    img_height, img_width = img.shape
    
    #create label array that stores the grey intensity level value of each pixel
    y = np.zeros(shape=img_height*img_width)
    
    #counter for y
    k=0
    for i in range(img_height):
        for j in range(img_width):
            y[k] = img[i,j]
            k+=1
    
    return y


# get vectors of out-degree, weighted out-degree and weighted in-degree
def get_feature_vectors(img, max_radius):
    max_intensity = 255
    img_height,img_width = img.shape
    
    X_out = np.zeros(shape=[img_height*img_width, max_radius])
    X_wout = np.zeros(shape=[img_height*img_width, max_radius])
    X_win = np.zeros(shape=[img_height*img_width, max_radius])
    
    G = icm.create_graph(img)
    
    for radius in range(max_radius):
        
        G.clear_edges()
        
        G = icm.connect_neighborhood(img, G, radius+1, max_intensity)
    
        X_out[:,radius], X_wout[:,radius], X_win[:,radius] = get_cn_measures(G)
    
    
    #apply z-score normalizer in all feature vectors
    std_scaler = StandardScaler()
    
    X_out = std_scaler.fit_transform(X_out)
    X_wout = std_scaler.fit_transform(X_wout)
    X_win = std_scaler.fit_transform(X_win)
    
    return X_out, X_wout, X_win

def get_image_signature(path_to_image,q, Q, max_radius):
    
    
    img = cv2.imread(path_to_image, cv2.IMREAD_GRAYSCALE)
    img = np.array(img, dtype=np.float32)
    
    
    F = get_signature(img, max_radius, Q)
    q.put(F)
    
    return F

    
def get_signature(img, max_radius, Q):

    #generate labels for the image (pixel intensity)
    y = get_labels_from_image(img)

    #generate feature matrices for the image modeled as a complex network
    X_out, X_wout, X_win = get_feature_vectors(img, max_radius)

    num_samples, num_attributes = X_out.shape
    
    F = np.array([], dtype=np.float32)
    for q in Q:
        rnn = RNN(num_samples=num_samples, 
                  num_attributes=num_attributes, num_hidden_neurons=q)
    
        rnn.set_hidden_weights(method='lcg')
    
        f_out = rnn.get_output_weights(X_out, y)
        f_wout = rnn.get_output_weights(X_wout,y)
        f_win = rnn.get_output_weights(X_win, y)
    
        F = np.concatenate((F,f_out,f_wout,f_win))

    return F




