#include<iostream>
#include"node.h"

using namespace std;

class Graph{
    private:
    int numVertices;
    Node** adjLists;

    public:

    Graph(int numVertices);

    int getNumVertices();
    Node** getAdjLists();
    void setNumVertices(int n_vertices);
    void setAdjLists(Node** adjLists);
    Node* createNode(int v);

    void printGraph();

    void addEdge(int src, int dest);

};
