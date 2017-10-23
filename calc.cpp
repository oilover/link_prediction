#include "calc.h"
default_random_engine random(time(NULL));
uniform_real_distribution<double> dis;
bool has_node(int u)
{
	return u<MAX_NODES && !my_sample[u].empty();
}
void add_node(int u)
{
	if (has_node(u)) return;
	hash_value[u] = dis(random);//(rand()) * (rand()) / RM;
	largest[u] = last_largest[u] = my_node(1,u);
}
void _add_sample(int u, my_node _v) // S[u]<==v
{
	largest[u] = max(largest[u], _v);
	my_sample[u].insert(_v);
}
void add_sample(int u,int v) // S[u]<==v
{
	my_node _v = my_node(hash_value[v], v);
	if (my_sample[u].size() < SAMPLE_LIM) {
		_add_sample(u,_v);
	} else {
		if (_v < largest[u]) {
			last_largest[u] = largest[u];
			my_sample[u].erase(largest[u]);
			_add_sample(u,_v);
			largest[u] = *max_element(my_sample[u].begin(), my_sample[u].end());
			//get_largest(my_sample[u]);
		}
	}
}
void add_edge(int u, int v)
{
	add_node(u); add_node(v);
	add_sample(u,v);
	add_sample(v,u);
}
double app_ratio(int u)
{
	return (largest[u].my_hash + last_largest[u].my_hash) / 2.0;
}
double app_cn(int u, int v)
{
	double ratio = max(app_ratio(u), app_ratio(v));
	set<my_node> si;
	set_intersection(my_sample[u].begin(), my_sample[v].begin(),
		my_sample[v].begin(), my_sample[v].end(),  inserter(si, si.begin()) );
	return 1.0 * si.size() / ratio;
}
set<int> toID(set<node_type> s)
{
    set<int> t;
    for (node_type x: s) t.insert(x.ID);
    return t;
}
vector<int> toID(vector<node_type> s)
{
    vector<int> t;
    for (node_type x: s) t.push_back(x.ID);
    return t;
}
template<class T>
vector<T> toVec(set<T> s)
{
    vector<T> v;
    for (T x: s) v.push_back(x);
}
template<class T>
vector<T> select(set<T> s)
{
    vector<T> v = toVec(s);
    shuffle (v.begin (), v.end (), std::default_random_engine (time(NULL)));
    if (v.size() > NEIGHBOR_LIM) v.resize(NEIGHBOR_LIM);
    return v;
}

vector<predict_item> enumerate()
{
   result;
    for (int u: nodes) {
        vector<my_node> vec = select(my_sample[u]);
        for (auto node: vec) {
            int mid = node.ID;
            auto vec2 = toID(select(my_sample[mid]));
            for (int v: vec2) {
                double cn = app_cn(u,v);
                if (cn > 0.5) {
                    result.push_back((predict_item){u,v,cn});
                }
            }
        }
    }
    sort(result.begin(), result.end());
    return result;
}
int main(int argc, char const *argv[])
{
	srand(time(NULL));
	// my_node t; prt(t.ID);
	// prt(RAND_MAX); puts("===");
	// prt(RAND_MAX*RAND_MAX); puts("===");1.0*rand()*rand()/RM
	// for (int i=0;i<10;i++) printf("%12d,",rand()*rand()); cout<<endl;
	freopen("a","w",stdout);
	for (int i=0;i<2000;i++) printf("%.8f,\t", dis(random)); cout<<endl;
	return 0;
}
