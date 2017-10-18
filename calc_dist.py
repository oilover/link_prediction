import time,random, numba
import sys, pickle
import networkx as nx
name = 'facebook-wosn-links' #'ca-cit-HepTh'
#'internet-growth.txt' #'flickr-growth-sorted.txt''ca-cit-HepPh' 
file_name = name+'/'+name+'.txt' 
Ja_file = file_name[:-4] + '--Ja.txt'
PA_file = file_name[:-4] + '--PA.txt'
CN_file = file_name[:-4] + '--CN.txt'
AA_file = file_name[:-4] + '--AA.txt'
distance_file = file_name[:-4] + '--distance.txt'
def sample_edges(G):
	E = int(G.number_of_edges() * 0.1)
	return random.sample(G.edges(), E)
def to_negative(res):
	return res[:-4]+'--negative.txt'
def sample_missing_edges(G, oldG, alpha=0.2):
	E = int(G.number_of_edges() * alpha)
	V = G.nodes()
	ret = set()
	while len(ret)<E:
		u,v = random.sample(V,2)
		if u>v: u,v=v,u
		if oldG.has_edge(u,v): continue
		if (not (u,v) in ret) and (not G.has_edge(u,v)): 
			ret.add((u,v))
	return ret


def calc_PA(G, newG):
	PA = list(nx.preferential_attachment(G, newG_E) )
	pickle.dump(PA, open(PA_file,'w'))
	PA = list(nx.preferential_attachment(G, sample_missing_edges(newG,G) ) )
	pickle.dump(PA, open(to_negative(PA_file),'w'))

def calc_disibution(G, newG):
	global newG_E
	newG_E = sample_edges(newG)

	Ja = list(nx.jaccard_coefficient(G, newG_E) )
	pickle.dump(Ja, open(Ja_file,'w'))
	Ja = list(nx.jaccard_coefficient(G, sample_missing_edges(newG,G) ) )
	pickle.dump(Ja, open(to_negative(Ja_file),'w'))

	calc_PA()


	CN = list(nx.cn_soundarajan_hopcroft(G, newG_E))  # long time
	pickle.dump(CN, open(CN_file,'w'))
	CN = list(nx.cn_soundarajan_hopcroft(G, sample_missing_edges(newG,G)))
	pickle.dump(CN, open(to_negative(CN_file),'w'))

	AA = list(nx.adamic_adar_index(G, newG_E) )
	pickle.dump(AA, open(AA_file,'w'))
	AA = list(nx.adamic_adar_index(G, sample_missing_edges(newG,G)) )
	pickle.dump(AA, open(to_negative(AA_file),'w'))
