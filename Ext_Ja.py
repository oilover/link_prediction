'''
	Digg: need to be sorted by timestamps (279,630 nodes and 1,731,653 directed edges) 170w
	wiki-growth: 1,870,709 nodes and 39,953,145 directed edges
'''
import time,random
import sys, pickle
import networkx as nx
name = 'digg-friends' #'ca-cit-HepPh'
#'internet-growth.txt' #'flickr-growth-sorted.txt''ca-cit-HepPh' 
file_name = name+'/'+name+'.txt' 
Ja_file = file_name[:-4] + '-Ja.txt'
CN_file = file_name[:-4] + '-common_neighbor.txt'
distance_file = file_name[:-4] + '--distance.txt'
AA_file = file_name[:-4] + '--AA.txt'
noden, edgen = 317080 , 1546540 # 104824 #1500000 #33140018
predict = {}
train_p = 0.5
lb_train = 3 # lower bound of degree in training graph
Core = set()
G = nx.Graph()
newG = nx.Graph()
Core = set()
def to_negative(str):
	return str[:-4]+'--negative.txt'

def sample_edges(G):
	E = int(G.number_of_edges() * 0.1)
	return random.sample(G.edges(), E)

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

def get_predict(G, Core):
	return []
	predict = set()
	num = 0;
	for u in Core:
		# if not u in newG.nodes(): continue;
		for v in G[u]:
			# if not v in newG.nodes(): continue;
			for U in set(G[v].keys()) & Core:
				# if not v in newG.nodes(): continue;
				if u>=U: continue
				if (u,U) in predict: continue
				num+=1
				predict.add((u,U))
	predict=nx.jaccard_coefficient(G,predict)
	print 'Predict complexity:',num
	return list(predict)

def calc_distribution(G, newG):
	newG_E = sample_edges(newG)

	Ja = list(nx.jaccard_coefficient(G, newG_E) )
	pickle.dump(Ja, open(Ja_file,'w'))
	Ja = list(nx.jaccard_coefficient(G, sample_missing_edges(newG,G) ) )
	pickle.dump(Ja, open(to_negative(Ja_file),'w'))

	CN = list(nx.cn_soundarajan_hopcroft(G, newG_E))  # long time
	pickle.dump(CN, open(CN_file,'w'))
	CN = list(nx.cn_soundarajan_hopcroft(G, sample_missing_edges(newG,G)))
	pickle.dump(CN, open(to_negative(CN_file),'w'))

	AA = list(nx.adamic_adar_index(G, newG_E) )
	pickle.dump(AA, open(AA_file,'w'))
	AA = list(nx.adamic_adar_index(G, sample_missing_edges(newG,G)) )
	pickle.dump(AA, open(to_negative(AA_file),'w'))

def Predict():
	prediction = sorted(predict, key=lambda x:x[-1], reverse=True)  #key=lambda x:x[-1]
	edgen_new = newG.number_of_edges()
	prediction = prediction[:edgen_new]
	print prediction[:10]
	ans = 0
	for x in prediction:
		u,v=x[:2]
		if newG.has_edge(u,v):
			ans+=1
	ans = 1.0*ans/newG.number_of_edges()
	print 'Precision:', ans
	N = len(Core)
	C = N*(N-1)/2 - G.number_of_edges();
	print 'Random precision:', newG.number_of_edges()*1.0/C
	print 'Relative precision:', ans*C/newG.number_of_edges()

if __name__ == '__main__':
	start_time = time.time()
	print time.ctime(start_time)
	i=1;
	G = nx.Graph()
	newG = nx.Graph()
	Core = set()
	
	train_edge_num = int(edgen*train_p)
	print ('Data: ',file_name)
	print ('train_edge_num:',train_edge_num)
	# fo = open(CN_file,'w')
	CN = []
	for line in open(file_name):
		str = line.split('\t')
		u,v=[int(x) for x in str[:2]]
		# 	if u>v: u,v=v,u
		if i<=train_edge_num:
			G.add_edge(u,v)
			if G.degree(u)==lb_train: Core.add(u)
			if G.degree(v)==lb_train: Core.add(v)
			if (i==train_edge_num): 
				print 'G.number_of_nodes():',G.number_of_nodes()
				print 'G.number_of_edges():',G.number_of_edges()
				print 'Core size:', len(Core)
				print 'Begin predict..'
				st=time.time()
				predict=get_predict(G, Core)
				print 'Predict finished, time: ', time.time()-st
		else: # predict			
			if (not u in Core) or (not v in Core):
				continue;
			newG.add_edge(u,v)	
			# if i==edgen: break		
		i+=1

	for u in G.nodes(): 
		G.node[u]['community'] = i
		i+=1 
	print 'newG.number_of_nodes():',newG.number_of_nodes()
	print 'newG.number_of_edges():',newG.number_of_edges()
	newG_E = sample_edges(newG)
	

	

	

	
	print ('Total time:',time.time()-start_time)
# Read finished..
# G.number_of_nodes(): 271153
# newG.number_of_nodes(): 216874
# newG.number_of_edges(): 443514
# [((181649, 301301), 1.0), ((209852, 349025), 1.0), ((193853, 241805), 1.0), ((154654, 324125), 1.0), ((171235, 176075), 1.0), ((138955, 424161), 1.0), ((173786, 207997), 1.0), ((266440, 292227), 1.0), ((303490, 370338), 1.0), ((115409, 191475), 1.0)]
# Precision: 0.179726006394
# Random precision: 0
# Relative precision: 14897.0687153
# [Finished in 582.7s]

# 
# Begin predict..
# G.number_of_nodes(): 271153
# G.number_of_edges(): 524933
# Begin predict..
# complexity: 5459662
# newG.number_of_nodes(): 216874
# newG.number_of_edges(): 443514
# [((181649, 301301), 1.0), ((209852, 349025), 1.0), ((193853, 241805), 1.0), ((154654, 324125), 1.0), ((171235, 176075), 1.0), ((138955, 424161), 1.0), ((173786, 207997), 1.0), ((266440, 292227), 1.0), ((303490, 370338), 1.0), ((115409, 191475), 1.0)]
# Precision: 0.179726006394
# Random precision: 0
# Relative precision: 14897.0687153
# [Finished in 147.3s]

# 0.75
# Begin predict..
# G.number_of_nodes(): 301722
# newG.number_of_nodes(): 185786
# newG.number_of_edges(): 241671
# complexity: ?
# [((230306, 232014), 1.0), ((280859, 391159), 1.0), ((265192, 331977), 1.0), ((304523, 396052), 1.0), ((224699, 224700), 1.0), ((211455, 291700), 1.0), ((185942, 357975), 1.0), ((335600, 377833), 1.0), ((202700, 400883), 1.0), ((26554, 29230), 1.0)]
# Precision: 0.147460804151
# Random precision: 5.30944995081e-06
# Relative precision: 27773.2732236
# [Finished in 398.7s]


# first 150w edges of  flickr
# G.number_of_nodes(): 135769
# G.number_of_edges(): 710541
# Begin predict..
# complexity: 1117554157
# Predict finished, time:  321.473999977
# # [Finished in 52.8s]

# input: facebook-sorted.txt ( sorted by timestamp, 90w edges )
# fg: 454982
# G.number_of_nodes(): 38374
# G.number_of_edges(): 313616
# Begin predict..
# Predict complexity: 8367741
# Predict finished, time:  229.565000057
# newG.number_of_nodes(): 28301
# newG.number_of_edges(): 114873
# [((52486, 52491), 1.0), ((55936, 55938), 1.0), ((52991, 52992), 1.0), ((30179, 46463), 1.0), ((52487, 52491), 1.0), ((44573, 44574), 1.0), ((36847, 42440), 1.0), ((57309, 60613), 1.0), ((29780, 43939), 1.0), ((48155, 55077), 1.0)]
# Precision: 0.0523969949422
# Random precision: 0.000156088232918
# Relative precision: 335.688308866
# [Finished in 402.8s]