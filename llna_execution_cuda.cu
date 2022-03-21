#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<dirent.h>
#include<string.h>
#include<stdbool.h>

#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#define NB_SIZE 8

typedef struct{
    bool rule[NB_SIZE+1];
}rules;

typedef struct node{
    int vertex;
    struct node* next;
}node;

node* createNode(int);

typedef struct{
    int numVertices;
    node** adjLists;
}Graph;

//Create a node
node* createNode(int v){
    node *newNode = (node*) malloc(sizeof(node));
    newNode->vertex = v;
    newNode->next = NULL;
    return newNode;
}

//Create a graph
Graph* createGraph(int vertices){
    Graph *graph = (Graph*) malloc(sizeof(Graph));
    graph->numVertices = vertices;

    graph->adjLists = (node**) malloc(vertices * sizeof(node*));

    int i;
    for(i=0; i<vertices;i++){
        graph->adjLists[i] = NULL;
    }

    return graph;
}

//Add edge (in bidirectional graph)
void addEdge(Graph* graph, int source, int destiny){
    //add edge from s to d
    node* newNode = createNode(destiny);
    newNode->next = graph->adjLists[source];
    graph->adjLists[source] = newNode;

}

//print the graph
void printGraph(Graph* graph) 
{
    int v;
    for (v=0; v<graph->numVertices;v++){
        node* temp = graph->adjLists[v];
        printf("\nVertex %d\n ", v);
        while(temp){
            printf("%d -> ", temp->vertex);
            temp = temp->next;
        }
        printf("\n");
    }
}

Graph* construct_graph_from_image(int rows, int cols, int *img, int R){

    //Create the graph
    Graph *G = createGraph(rows*cols);

    for (int i=0;i<rows;i++){
        for(int j=0;j<cols;j++){
            for(int y=i-R;y<=i+R;y++){
                if(y >= 0 && y<rows){
                    for(int x=j-R;x<=i+R;x++){
                        if(x >= 0 && x<cols){
                            double d = sqrt(pow(i-y,2)+pow(j-x,2));
                            if(img[j+i*cols] <= img[x+y*cols] && d<=R){
                                addEdge(G, j+i*cols,x+y*cols);
                            }
                        }
                    }
                }
            }
        }
    }
    
    return G;

}

rules* getAllRules(){
    rules *allRules = (rules*) malloc(sizeof(rules)*512);

    int counter=0;

    FILE *ruleFile;
    char *rulePath = "data/rules/rules.csv";

    ruleFile = fopen(rulePath, "r");
    rules *pRules = &allRules[counter];
    while(1){
        char c=fgetc(ruleFile);
        if(c== EOF){
            break;
        }
        else if(c == '\n'){
            counter++;
            pRules = &allRules[counter];
        }
        else if(c != ','&& c != ' '){
            allRules[counter].rule[(int)c-48]=true;
        }
    }
    return allRules;
}

bool isInList(int array[], int value){
    int size = sizeof(array)/sizeof(array[0]);


    for(int i=0;i < size; i++){
        if(array[i]==value)
            return true;
    }
    return false;
}

void generateAllTep(rules* bRules, rules *sRules, Graph *G, int number_of_nodes, int steps){

    int counterB = 0;
    int counterS = 0;
    
    double density[number_of_nodes];
    double resolution[NB_SIZE+1];

    for(int i=0;i<NB_SIZE+1;i++){
        resolution[i] = i+1/(double)NB_SIZE+1;
    }

    FILE *rules = fopen("data/rules/rules.csv", "r");

    while(counterB < 512){
        counterS=0;
        printf("\nBirth Rule number %d\n", counterB);
        while(counterS < 512){
            bool TEP[steps][number_of_nodes];
            for(int i=0;i<number_of_nodes;i++){
                TEP[0][i] = rand() & 1;
            }
            for(int i=1;i<steps;i++){
                for(int j=0;j<number_of_nodes;j++){
                    int degree=0;
                    int num_neighbors_alive=0;
                    node *p = G->adjLists[j];
                    while(p){
                        p = p->next;
                        degree++;
                        if(TEP[i-1][j]==1){
                            num_neighbors_alive+=1;
                        }
                    }
                    density[i] = (double)num_neighbors_alive/(double)degree;
                    if(TEP[i-1][j] == 0){
                        for(int k=0;k<NB_SIZE+1;k++){
                            if(bRules[counterB].rule[k] == true && density[i] >= resolution[k] && density[i] < resolution[k+1]){
                                TEP[i][j]=1;
                                break;
                            }
                            TEP[i][j]=0;
                        }
                    }
                    else{
                        for(int k=0;k<NB_SIZE+1;k++){
                            if(sRules[counterS].rule[k] == true && density[i] >= resolution[k] && density[i] < resolution[k+1]){
                                TEP[i][j]=1;
                                break;
                            }
                            TEP[i][j]=0;
                        }  
                    }
                }
            }
            counterS++;
        }
        counterB++;
    }

}

const char *get_filename_ext(const char *filename){
    const char *dot = strrchr(filename, '.');
    if(!dot || dot == filename) return "";
    return dot + 1;
}

void generateTepGPU(rules* bRules, rules *sRules, Graph *G, int number_of_nodes, int steps){

    int counterB = 0;
    int counterS = 0;
    
    double density[number_of_nodes];
    double resolution[NB_SIZE+1];

    for(int i=0;i<NB_SIZE+1;i++){
        resolution[i] = i+1/(double)NB_SIZE+1;
    }

    dim3 block_size(128);
    dim3 grid_size(8);

    Graph *gpu_graph;
    cudaMalloc((void**) &gpu_graph, sizeof(G));
    cudaMemcpy(gpu_graph, G, sizeof(G), cudaMemcpyHostToDevice);

    FILE *rules = fopen("data/rules/rules.csv", "r");

    while(counterB < 512){
        counterS=0;
        printf("\nBirth Rule number %d\n", counterB);
        while(counterS < 512){
            bool TEP[steps][number_of_nodes];
            cudaMalloc((void**) &TEP, sizeof(TEP));

            rule* gpu_bRule;
            cudaMalloc((void**)&gpu_bRule, sizeof(rules));
            rule* gpu_sRule;
            cudaMalloc((void**)&gpu_sRule, sizeof(rules));

            cudaMemcpy(bRules[counterB], gpu_bRule, sizeof(rules),cudaMemcpyDeviceToHost);
            cudaMemcpy(sRules[counterS], gpu_sRule, sizeof(rules),cudaMemcpyDeviceToHost);

            for(int i=0;i<number_of_nodes;i++){
                TEP[0][i] = rand() & 1;
            }
            for(int i=1;i<steps;i++){
                execution_step(TEP, i, number_of_nodes, resolution, gpu_graph, gpu_bRule, gpu_sRule);
            }
            counterS++;
        }
        counterB++;
    }

}

__global__ void execution_step(int** TEP, int iter, int number_of_nodes, double* resolution, 
Graph* G, rules* bRule, rules *sRule){

    int gid = blockIdx.x * blockDim.x + threadIdx.x;

    int degree = 0;
    int num_neighbors_alive=0;
    node *p = G-> adjLists[iter];

    while(p){
        p = p->next;
        degree++;
        if(TEP[i-1][j]==1){
                num_neighbors_alive+=1;
        }
    }
    density[i] = (double)num_neighbors_alive/(double)degree;
    if(TEP[i-1][j] == 0){
        for(int k=0;k<NB_SIZE+1;k++){
            if(bRule.rule[k] == true && density[iter] >= resolution[k] && density[iter] < resolution[k+1]){
                TEP[i][j]=1;
                break;
            }
            TEP[i][j]=0;
        }
    }
    else{
        for(int k=0;k<NB_SIZE+1;k++){
            if(sRules[counterS].rule[k] == true && density[i] >= resolution[k] && density[i] < resolution[k+1]){
                TEP[i][j]=1;
                break;
            }
            TEP[i][j]=0;
        }
    }
å}

int main(void){
    rules *bRules = getAllRules();
    rules *sRules = getAllRules();

    int steps = 350;

    int R=11;
    struct dirent *dir;
    DIR *d;
    char *sdir = (char*) malloc(sizeof(char)*30);
    sprintf(sdir, "data/USPTex/matrices/");
    d = opendir(sdir);
    int counter = 1;
    if(d){
        while((dir = readdir(d)) != NULL){
            if(!strcmp(get_filename_ext(dir->d_name), "txt")){
                printf("Iniciando imagem %d\n", counter);
                FILE *matrix;
                char *path = (char*) malloc(sizeof(char)*30);
                strcpy(path, sdir);
                strcat(path, dir->d_name);
                matrix = fopen(path, "r");

                int value;
                int size;
                 
                fscanf(matrix, "%d", &size);

                int *img = (int*)malloc(sizeof(int)*size);
                int i=0;
                while(fscanf(matrix, "%d", &value)!= EOF){
                    img[i]=value;
                    i++;
                }
                
                int rows = sqrt(size);
                int cols = sqrt(size);

                fclose(matrix);


                Graph *G = construct_graph_from_image(rows, cols, img,R);

                generateAllTep(bRules,sRules, G, rows*cols, steps);

                counter++;

                free(path);
            }
            
        }
    }
    closedir(d);

    return 0;
}


