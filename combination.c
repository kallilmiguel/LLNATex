#include <stdio.h>
#include <stdlib.h>

void makeCombination(FILE *rules,int arr1[], int data[], int st, int end, int index, int r){

    if(index == r)
    {
        for(int j=0; j<r; j++){
            if(j==r-1){
                printf("%d", data[j]);
                fprintf(rules,"%d", data[j]);
            }
            else{
                printf("%d, ", data[j]);
                fprintf(rules,"%d, ", data[j]);
            }   
            
        }
        printf("\n");
        fprintf(rules,"\n");
        return;
    }
    for (int i=st; i<=end && end-i+1 >= r-index; i++){
        data[index] = arr1[i];
        makeCombination(rules, arr1, data, i+1, end, index+1, r);
    }
}

void CombinationDisplay(FILE *rules, int arr1[], int n, int r){
    int data[r];
    makeCombination(rules, arr1, data, 0, n-1, 0, r);
}

int main(void){

    FILE *bRules;

    int arr1[] = {0,1,2,3,4,5,6,7,8};
    int R=9;
    int n = sizeof(arr1)/sizeof(arr1[0]);

    char *path = "data/rules/rules.csv";

    bRules = fopen(path, "w");

    printf("The given array is: \n");
    for(int i=0; i<n; i++){
        printf("%d ", arr1[i]);
    }
    printf("\n");
    for(int r=1;r<=R;r++){
        printf("The combination from by the number of elements are: %d\n", r);
        printf("The combinations are: \n");
        CombinationDisplay(bRules, arr1, n, r);
    }
    
    fclose(bRules);

}
