#include <iostream>
#include "graph.h"
using namespace std;


Graph::Graph(int numVertices){
    this->numVertices = numVertices;

    this->adjLists = (Node**) malloc(sizeof(Node*)*numVertices);

    int i;
    for(i=0; i<numVertices;i++){
        this->adjLists[i] = NULL;
    }

}

int Graph::getNumVertices(){
    return this->numVertices;
}

Node** Graph::getAdjLists(){
    return this->adjLists;
}

void Graph::setNumVertices(int n_vertices){
    this->numVertices = n_vertices;
}

void Graph::setAdjLists(Node** adjLists){
    this->adjLists = adjLists;
}

Node* Graph::createNode(int v){
    Node *newNode = (Node*) malloc(sizeof(Node));

    newNode->vertex = v;
    newNode->next = NULL;
    return newNode;
}

void Graph::addEdge(int src, int dest){
    Node* newNode = this->createNode(dest);

    newNode->next = this->adjLists[src];
    this->adjLists[src] = newNode;
}

void Graph::printGraph(){
    int v;
    for (v=0; v<this->numVertices;v++){
        Node* temp = this->adjLists[v];
        cout << "\nVertex " << v << "\n";
        while(temp){
            cout << temp->vertex << " -> ";
            temp = temp->next;
        }
        printf("\n");
    }
}
