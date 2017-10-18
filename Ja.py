import random, numba
lb_train = 20 # lower bound of degree in training graph
### Approximate Jaccard Begin ###
K = 50
H,my_hash,my_ID = {},{},{}#[{}] * K
G = {} #nx.Graph()
newG = {} #nx.Graph()
Core_num = 5000

def Add(*nodes): # when every edge arrive, call this method
	global G,newG,H,my_hash,my_ID
	for u in nodes:
		if not u in G: G[u]=1
		else :G[u]+=1 
		if G[u]>=lb_train and (not u in my_hash): 
			my_hash[u] = [random.random() for i in range(K)] 
			H[u] = [1] * K
			my_ID[u] = [u] * K
		
@numba.jit
def App_Ja(u,v):
	cnt=0
	for i in range(K): 
		if u in my_ID[i] and my_ID[i][u]==my_ID[i][v]: cnt+=1
	return 1.0*cnt/K

def _update(u,v):
	for k in range(K):		
		if H[u][k] > my_hash[v][k]: 
			H[u][k], my_ID[u][k] = my_hash[v][k], v
def update(u,v):
	Add(u,v)
	if u in H and v in H:
		_update(u,v)
		_update(v,u)
	pass
def Size(): return len(H)
### Approximate Jaccard End ###