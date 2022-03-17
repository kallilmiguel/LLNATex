#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<dirent.h>
#include<string.h>

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
    node *newNode = malloc(sizeof(node));
    newNode->vertex = v;
    newNode->next = NULL;
    return newNode;
}

//Create a graph
Graph* createGraph(int vertices){
    Graph *graph = malloc(sizeof(Graph));
    graph->numVertices = vertices;

    graph->adjLists = malloc(vertices * sizeof(node*));

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

Graph* construct_graph_from_image(int rows, int cols, int *img, int L, int R){

    //Create the graph
    Graph *G = createGraph(rows*cols);

    double weight;
    for (int i=0;i<rows;i++){
        for(int j=0;j<cols;j++){
            for(int y=i-R;y<=i+R;y++){
                if(y >= 0 && y<rows){
                    for(int x=j-R;x<=i+R;x++){
                        if(x >= 0 && x<cols){
                            weight=0;
                            double d = sqrt(pow(i-y,2)+pow(j-x,2));
                            if(img[j+i*cols] <= img[x+y*cols] && d<=R){
                                int diff = abs(img[j+i*cols] - img[x+y*cols]);
                                if(R==1){
                                    weight= (double) diff/L;
                                }
                                else{
                                    weight = ((d-1)/(double)(R-1) + diff/(double)L)/2;
                                }
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

const char *get_filename_ext(const char *filename){
    const char *dot = strrchr(filename, '.');
    if(!dot || dot == filename) return "";
    return dot + 1;
}

int main(void){

    int L=255;
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


                Graph *G = construct_graph_from_image(rows, cols, img,L,R);
                counter++;

                free(path);
            }
            
        }
    }
    closedir(d);

    return 0;
}

