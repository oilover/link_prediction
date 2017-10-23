#include "calc.h"

bool has_node(int u)
{
	return u<MAX_NODES && !my_sample[u].empty();
}
void add_node(int u)
{
	if (has_node(u)) return;
	hash_value[u] = (rand()) * (rand()) / RM;
	largest[u] = last_largest[u] = my_node(1,u);
}
void _add_sample(int u, my_node _v) // S[u]<==v
{
	largest[u] = max(largest[u], _v);
	my_sample[u].insert(_v);
}
void add_sample(int u,int v) // S[u]<==v
{
	auto _v = my_node(hash_value[v], v);
	if (my_sample[u].size() < SAMPE_LIM) {
		_add_sample(u,_v);
	} else {
		if (_v < largest[u]) {
			last_largest[u] = largest[u];
			my_sample[u].remove(largest[u]);
			_add_sample(u,_v);
			largest[u] = get_largest(my_sample[u]);
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
	return (largest[u].hash_value + last_largest[u].hash_value) / 2.0;
}
double app_cn(int u, int v)
{

}
int main(int argc, char const *argv[])
{
	srand(time(NULL));
	my_node t; prt(t.ID);
	prt(RAND_MAX); puts("===");
	prt(RAND_MAX*RAND_MAX); puts("===");
	for (int i=0;i<20;i++) printf("%12d",rand()*rand()); cout<<endl;
	return 0;
}