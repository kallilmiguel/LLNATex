#include<iostream>
#include"LLNA.h"

using namespace std;

LLNA::LLNA(int number_of_cells, int steps){
    
    this->setNumberOfCells(number_of_cells);
    this->setSteps(steps);

    this->TEP = new bool* [steps];

    for(int i=0; i<steps; i++){
        this->TEP[i] = new bool[number_of_cells];
    }

    this->density = (double*) malloc(sizeof(double)*number_of_cells);
    this->alive_neighbors = (int*)malloc(sizeof(double)*number_of_cells);
}

void LLNA::setNumberOfCells(int number_of_cells){
    this->number_of_cells = number_of_cells;
}

int LLNA::getNumberOfCells(){
    return this->number_of_cells;
}

void LLNA::setSteps(int steps){
    this->steps = steps;
}

int LLNA::getSteps(){
    return this->steps;
}