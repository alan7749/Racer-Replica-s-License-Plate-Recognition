#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// gcc -shared -fPIC speedup_performance.c -o speedup_performance.so
int ** calculate_cluster(int ** arr, int ** centroid, int black_len, int k) {
    // [which cluster, dot to cluster's distence]
    int ** cluster;
    int rows = black_len; // 行数
    int cols = 2; // 列数


    // 分配一维指针数组的内存
    cluster = (int **)calloc(rows, sizeof(int *));

    // 分配每行的内存
    for (int i = 0; i < rows; i++) {
        cluster[i] = (int *)calloc(cols, sizeof(int));
    }

    for(int i = 0;i < black_len;i++){
        for(int j = 0;j < k;j++){
            if(j != 0 && pow((arr[i][0] - centroid[j][0]), 2) + pow((arr[i][1] - centroid[j][1]), 2) < cluster[i][1]){
                cluster[i][0] = j;
                cluster[i][1] = pow((arr[i][0] - centroid[j][0]), 2) + pow((arr[i][1] - centroid[j][1]), 2);
            }
            else if(j == 0){
                cluster[i][0] = j;
                cluster[i][1] = pow((arr[i][0] - centroid[j][0]), 2) + pow((arr[i][1] - centroid[j][1]), 2);
            }
        }
    }
    return cluster;
}
int ** update_centroid(int ** cluster, int cluster_len, int k, int ** black_dot_list){
    int ** coordi;
    int rows = k; // 行数
    int cols = 2; // 列数
    int * total;
    // 分配一维指针数组的内存
    coordi = (int **)calloc(rows, sizeof(int *));
    total = (int *)calloc(rows, sizeof(int));

    // 分配每行的内存
    for (int i = 0; i < rows; i++) {
        coordi[i] = (int *)calloc(cols, sizeof(int));
    }

    for(int i = 0;i < cluster_len;i++){ // cluster[i][0] = which cluster, cluster[i][0] = distence
        coordi[cluster[i][0]][0] += black_dot_list[i][0]; // black_dot_list[i][0] = x
        coordi[cluster[i][0]][1] += black_dot_list[i][1]; // black_dot_list[i][1] = y
        total[cluster[i][0]] += 1;
    }
    for(int i = 0;i < k;i++){
        coordi[i][0]  = coordi[i][0] / total[i];
        coordi[i][1]  = coordi[i][1] / total[i];
    }
    return coordi;
}
int ** create_coordinate(int ** img, int h, int w){
    int ** black_dot_list;
    int total = 0;
    // 分配一维指针数组的内存
    black_dot_list = (int **)calloc(h * w, sizeof(int *));
    for (int i = 0; i < h * w; i++) {
        black_dot_list[i] = (int *)calloc(2, sizeof(int));
    }
    for(int i = 0;i<h;i++){
        for(int j = 0;j<w;j++){
            if(img[i][j] == 0){
                black_dot_list[total][0] = i;
                black_dot_list[total][1] = j;
            }
            total += 1;
        }
    }
    return black_dot_list;
}

int *mix_rotate_calculate(int h, int w, int **rotated){
    
    
    int *sum_h;
    int *sum_w;
    sum_h = (int *)calloc(h, sizeof(int));
    sum_w = (int *)calloc(w, sizeof(int));
    int avg = 0;
    for(int i = 0;i < h;i++){
        for(int j = 0;j < w;j++){
            if(rotated[i][j] == 0){
                sum_h[i] += 1; // 紀錄整張圖片每個row的黑點數
                sum_w[j] += 1; // 紀錄整張圖片每個col的黑點數
            }
        }        
    }
    int total = 0;
    for(int i = 0;i < h;i++){
        if(sum_h[i] != 0){  // 有黑點的row的數量
            avg = avg + sum_h[i];
            total += 1;
        }
    }
    
    avg = (int)(avg / total);
    // printf("plate_len: %d\n", plate_len);
    // printf("avg: ==============%d\n", avg);

    int little = 0;
    for(int i = 0;i < w;i++){
        if(sum_w[i] != 0){
            little = i;
            break;
        }
    }
    int big = 0;
    for(int i = w - 1;i >= 0;i--){
        if(sum_h[i] != 0){
            big = i;
            break;
        }
    }
    int plate_len = big - little;
    int *res;
    res = (int *)calloc(2, sizeof(int));
    res[0] = plate_len;
    res[1] = avg;
    return res;
}