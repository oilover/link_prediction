import time,random, numba
import sys, pickle
import networkx as nx
from time import ctime
name = 'facebook-wosn-links' #'ca-cit-HepTh'
#'internet-growth.txt' #'flickr-growth-sorted.txt''ca-cit-HepPh' 
file_name = name+'/'+name+'.txt' 
noden, edgen = 317080 , 335708
#2444798
#3148447 #1546540 # 104824 #1500000 #33140018
predict = []
train_p = 0.5
lb_train = 5 # lower bound of degree in training graph
Core = set()
G = {} #nx.Graph()
newG = {} #nx.Graph()
Core_num = 5000

def Add(*nodes): # when every edge arrive, call this method
	global G,newG
	for u in nodes:
		if not u in G: G[u]=1
		else :G[u]+=1 
		if G[u]==lb_train: Core.add(u)

def prune_Core():

if __name__ == '__main__':
	G = nx.Graph()
	newG = nx.Graph()
	Core = set()
	train_edge_num = int(edgen*train_p)
	i=1
	print ('Data: ',file_name)
	print ('train_edge_num:',train_edge_num)
	for line in open(file_name):
		str = line.split('\t')
		u,v=[int(x) for x in str[:2]]
		# 	if u>v: u,v=v,u
		if i<=train_edge_num:
			G.add_edge(u,v)
			if G.degree(u)==lb_train: Core.add(u)
			if G.degree(v)==lb_train: Core.add(v)
		else: # predict			
			newG.add_edge(u,v)	
			# if i==edgen: break		
		i+=1
	NC = set()
	for u in Core:
		if u in newG and newG.degree(u)>=lb_train: NC.add(u)
	Core = NC
	pickle.dump(Core,open(file_name[:-4] + '--Core-all.txt','w'))
	if len(Core)>Core_num: Core = set(random.sample(Core, Core_num) )
	e1 = G.subgraph(Core).number_of_edges()
	e2 = newG.subgraph(Core).number_of_edges()
	pickle.dump([Core,e1,e2],open(file_name[:-4] + '--Core.txt','w'))
	print Core[:5],e1,e2