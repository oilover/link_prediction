#ifndef CALC_H
#define CALC_H
#include <bits/stdc++.h>
using namespace std;
#define prt(k) cerr<<#k" = "<<k<<"\t"
typedef long long LL;
typedef pair<int,int> my_node; // hash value, ID
typedef pair<int,int> node_type; // hash value, ID
#define ID second
#define my_hash first
const int MAX_NODES = 2001000; // maybe 330w
const int NEIGHBOR_LIM = 20; // limit when enumerate 2-hop beighbors
const int SAMPLE_LIM = 80; // L in paper
const int RM = RAND_MAX * RAND_MAX;
set<my_node>  my_sample[MAX_NODES];
set<int> nodes;
double hash_value[MAX_NODES];
my_node largest[MAX_NODES], last_largest[MAX_NODES];
bool has_node(int u);
void add_node(int u);
void _add_sample(int u, my_node _v);
void add_sample(int u,int v);
void add_edge(int u, int v);
double app_ratio(int u);
double app_cn(int u, int v);
struct predict_item
{
    int u, v;
    double val;
    bool operator < (predict_item b) const
    {
        return val > b.val;
    }
};
#endif // CALC_H
