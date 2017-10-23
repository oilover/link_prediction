#include <bits/stdc++.h>
using namespace std;
#define prt(k) cerr<<#k" = "<<k<<"\t"
typedef long long LL;
typedef pair<int,int> PII;
const int MAXV = 100100;
const int MAXK = 108;
const int K = 50;
double H[MAXK][MAXV];
double h[MAXK][MAXV];
double I[MAXK][MAXV];
double App_Ja(int u , int v)
{
    int cnt=0;
    for (int i=0;i<K;i++) cnt+=(I[i][u]==I[i][v]);
    return 1.0*cnt/K;
}
class Graph
{
    int N,M;
    set<int> nodes;
    vector<set<int> > edges;
    vector<PII> edge_list;
  //  const static int SIZE = 100;
public:
    Graph(int SIZE=100) {
        srand(time(NULL));
        nodes.clear(); N=M=0; edges.resize(SIZE);
        for(auto u:edges)u.clear();
    }
    void number_of_nodes() {
        return nodes.size();
    }
    void number_of_edges() {
        return M;
    }
    void get_nodes()
    {
        return nodes;
    }
    void update(int u, int v)
    {
        if (h[k][v] < H[k][u]) {
            I[k][u] = v;
            H[k][u] = h[k][v];
        }
    }
    void Update(int u, int v)
    {
        update(u,v); update(v,u);
    }
    void add_node(int u) {
        if(nodes.count(u)) return;
        for (int i=0;i<K;i++) {
            h[i][u] = rand();
            H[i][u] = 1;
            I[i][u] = u;
        }
        nodes.insert(u);
    }
    void add_empty_edge(int u, int v)
    {
        add_node(u); add_node(v);
        Update(u,v);
        M++;
    }
    void add_edge(int u, int v)
    {
        int uu = max(u,v);
        if (edges.size()<=uu) edges.resize(uu+1);
        if (edges[u].count(v)) return;
        M++;
        if (u>v) swap(u,v);
        add_node(u); add_node(v);
        edge_list.push_back(PII(u,v));
        edges[u].insert(v);
        edges[v].insert(u);
    }
    bool has_edge(int u, int v)
    {
        return edges[u].count(v);
    }
};
