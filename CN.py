### Approximate CN ###
sample_size,hash_value={},{}
Largest = {}
import random
L=80
def add_node(*nodes):
	global Largest,sample_size,hash_value
	for u in nodes:
		if not u in hash_value:
			hash_value[u]=random.random()
			Largest[u]=(1,1,1)
			sample_size[u]=0
def my_replace(y,x):
	l1,l2,l3=y
	if l1<x: return l1,l2,l3
	if l2<x: return x,l2,l3
	if x>l3: return l2,x,l3
	return l2,l3,x
def calc(t): # t=Largest[u]
	if t[0]==1: return (t[1]+t[2])/2
	return (t[0]+t[1])/2
def add_sample(u,v): # S(u)<--v
	if sample_size[u]<L:
		sample_size[u]+=1
		Largest[u] = my_replace(Largest[u],hash_value[v])
def add_edge(u,v):
	global sample_size,hash_value,Largest
	add_node(u,v)
	add_sample(u,v)
	add_sample(v,u)
	
