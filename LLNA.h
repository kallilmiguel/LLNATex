#include <iostream>
#include <graph.h>

using namespace std;

class LLNA{

    private:
    int number_of_cells;
    int steps;
    int* alive_neighbors;
    double* density;
    bool** TEP;
    bool* bRule;
    bool* sRule;
   
    public:
    LLNA(int number_of_cells, int steps);

    void setNumberOfCells(int n_cells);
    void setSteps(int steps);
    int getNumberOfCells();
    int getSteps();

    void setBrule(bool bRule[]);
    void setSrule(bool sRule[]);

    void evolveTEP()
    
};