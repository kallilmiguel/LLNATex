#include<iostream>
#include"graph.h"

using namespace std;

int main(void){
    Graph G(5);

    G.addEdge(1,5);
    G.addEdge(2,3);
    G.addEdge(1,4);
    G.addEdge(3,4);

    G.printGraph();
}
