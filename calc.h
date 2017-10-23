#ifndef CALC_H
#define CALC_H
#include <bits/stdc++.h>
using namespace std;
#define prt(k) cerr<<#k" = "<<k<<"\t"
typedef long long LL;
typedef pair<int,int> my_node; // hash value, ID
#define ID second
#define my_hash first
const int MAX_NODES = 2001000; // maybe 330w
const int NEIGHBOR_LIM = 20; // limit when enumerate 2-hop beighbors
const int SAMPLE_LIM = 80; // L in paper
const int RM = RAND_MAX * RAND_MAX;
set<my_node>  my_sample[MAX_NODES];
double hash_value[MAX_NODES];
my_node largest[MAX_NODES], last_largest[MAX_NODES];
bool has_node(int u);

#endif // CALC_H
