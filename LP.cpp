#include <bits/stdc++.h>
#include "calc.h"
using namespace std;
#define prt(k) cerr<<#k" = "<<k<<"\t"
typedef long long LL;
#include "Graph.h"

const char file_name[]="facebook-wosn-links/facebook-wosn-links.txt";
int N, M;
int Core_num = 4000;
const int edge_num = 335708;
const int train_edge_num = edge_num * 0.5; // train ratio p=0.5

vector<pair<double, PII> > get_predict(vector<int> Core)
{
    int n = Core.size();
    sort(Core.begin(), Core.end());
    vector<pair<double, PII> > v;
    for (int i=0;i<n;i++) {
        for (int j=i+1;j<n;j++) {
            int u=core[i], v=Core[j];
            double s = App_Ja(u,v);
            if (s<0.02) continue;
            v.push_back(make_pair(s, PII(u,v)));
        }
    }
    sort(v.begin(), v.end());
    reverse(v.begin(), v.end());
    return v;
}
template<typename T>
set<T> V2S(std::vector<T> v) {
    set<T> s;
    for (T x: v) s.insert(x);
    return s;
}
int main()
{
    freopen(file_name,"r",stdin);
    M = 0;
    int start_time = time(NULL);
    int u,v, t; char buf[123];
//    printf("adsfasfasfas\n");
    Graph G = Graph();
    Graph newG;
    vector<int> nodes;
    set<int> Core;
    while (gets(buf)!=NULL) {
        char tmp_str[55];++M;
        sscanf(buf, "%d\t%d\t%d\t%s\n",&u,&v,&t,tmp_str);
        vector<pair<double, PII> > prediction;
//        printf("%d\t%d\n",u,v); //prt(buf);
        if (M<=train_edge_num) {
            G.add_empty_edge(u,v);
            update(u,v);
            if (M==train_edge_num) {
                set<int> node_set = G.get_nodes();
                
                copy(node_set.begin(),node_set.end(), back_inserter(nodes));
                shuffle(nodes.begin(),nodes.end(), std::default_random_engine(time(NULL)) );
                nodes.resize(Core_num);
                Core = V2S(nodes);
                prediction = get_predict(nodes);
            }
        }
        else {
            if (Core.count(u)&&Core.count(v)) {
                newG.add_edge(u,v)
            }
        }
    }
    E = newG.number_of_edges();
    double ans = 0;
    for (int i=0;i<min(E,prediction.size()); i++)  {
        int u=prediction[i][1][0], v=prediction[i][1][1];
        if (newG.has_edge(u,v)) ans++;
    }
    ans /= E;
    printf("Precision: %.4f\n", ans);
    N = Core_num;
    M = 
    int C = N*(N-1)/2 - G.number_of_edges();
}
