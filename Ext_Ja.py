'''
	Digg: need to be sorted by timestamps (279,630 nodes and 1,731,653 directed edges) 170w
	wiki-growth: 1,870,709 nodes and 39,953,145 directed edges
'''
import time,random, numba
import sys, pickle
import networkx as nx
from time import ctime
name = 'facebook-wosn-links' #'ca-cit-HepTh'
#'internet-growth.txt' #'flickr-growth-sorted.txt''ca-cit-HepPh' 
file_name = name+'/'+name+'.txt' 
Ja_file = file_name[:-4] + '--Ja.txt'
PA_file = file_name[:-4] + '--PA.txt'
CN_file = file_name[:-4] + '--CN.txt'
AA_file = file_name[:-4] + '--AA.txt'
distance_file = file_name[:-4] + '--distance.txt'

noden, edgen = 317080 , 335708
#2444798
#3148447 #1546540 # 104824 #1500000 #33140018
predict = []
train_p = 0.5
lb_train = 5 # lower bound of degree in training graph
Core = set()
G = nx.Graph()
newG = nx.Graph()
Core_num = 1000
newG_E = []
global ans,e1,e2,K,H,h,I,is_App,had_Core  # correctly predicted edges
e1,e2 = 774, 303  # e2: new raise edges
### Approximate Jaccard Begin ###
K = 10
H = [{} for i in range(K)]
h = [{} for i in range(K)]
I = [{} for i in range(K)]
is_App = True #whether or not use approximate algorithm
@numba.jit
def App_Ja(u,v):
	cnt=0
	for i in range(K): 
		if u in I[i] and I[i][u]==I[i][v]: cnt+=1
	return 1.0*cnt/K
@numba.jit
def update(u,v):
	for k in range(K):
		if not u in h[k]: h[k][u] = random.random()
		if not v in h[k]: h[k][v] = random.random()
		if not u in H[k] or h[k][v]<H[k][u]: 
			H[k][u] = h[k][v]
			I[k][u] = v
		if not v in H[k] or h[k][u]<H[k][v]:
			H[k][v] = h[k][u]
			I[k][v] = u
	pass
### Approximate Jaccard End ###
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

def my_jaccard(G,u,v):
	Nu,Nv = G.neighbors(u),G.neighbors(v)
	return 1.0*len(Nu&Nv)/len(Nu|Nv)
def calc_PA():
	PA = list(nx.preferential_attachment(G, newG_E) )
	pickle.dump(PA, open(PA_file,'w'))
	PA = list(nx.preferential_attachment(G, sample_missing_edges(newG,G) ) )
	pickle.dump(PA, open(to_negative(PA_file),'w'))

def calc_distribution(G, newG):
	# if not newG_E or len(newG_E)<10: newG_E = sample_edges(newG)

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


def RP(N,e1,e2): # Random precision
	C = N*(N-1)/2 - e1
	return 1.0*e2/C

def print_result():
	print ans,'/',e2
	ans = 1.0*ans/e2
	print 'Precision:', ans
	print 'e1:',e1
	rp = RP(len(Core), e1,e2)
	print 'Random precision:', rp
	if ans: print 'Relative precision:', ans/RP
# @numba.jit
def calc_predict(Core):
	print 'Begin predict..'
	st=time.time()
	predict = []
	num = 0;
	tt = time.time()
	for u in Core:
		Space = Core
		if u in G: Space = Core - set(G[u].keys())
		# if random.random()<0.01: print 'len(Space):',len(Space)
		for v in Space:
			if u>=v: continue
			num+=1			
			if is_App:
				t = [[u,v,App_Ja(u,v)]]
			else:
				t = list(nx.jaccard_coefficient(G,[(u,v)]))
			if (num%500000==0): print t,num,len(predict),time.time()-tt,ctime(time.time())
			if t[0][-1]>0.01: 
				predict.append(t[0])
				# if len(predict)<8: print t

	# print 'Predict complexity:',num
	print ('len(predict):', len(predict))
	print 'Predict finished, time: ', time.time()-st
	predict.sort(key=lambda x:x[-1], reverse=True)  #key=lambda x:x[-1]
	subG = newG.subgraph(Core)
	predict = predict[:e2]
	print '5 of predict:', predict[:5]
	predict = set([(u,v) for (u,v,p) in predict])
	return predict
	ans = 0
	for x in predict:
		u,v=x[:2]
		if newG.has_edge(u,v):
			ans+=1
	print_result()

had_Core = True # Core shifou shixian write into file
def main():
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
	if had_Core:
		Core = pickle.load(open(file_name[:-4] + '--Core.txt'))
	ans = 0
	for line in open(file_name):
		str = line.split('\t')
		u,v=[int(x) for x in str[:2]]
		# 	if u>v: u,v=v,u
		if i<=train_edge_num:
			if not is_App: G.add_edge(u,v)
			# if u in Core and v in Core: e1+=1
			if not had_Core:
				if G.degree(u)==lb_train: Core.add(u)
				if G.degree(v)==lb_train: Core.add(v)
			if had_Core and (u in Core or v in Core) and is_App:
				update(u,v)
			if (i==train_edge_num): 
				# print 'G.number_of_nodes():',G.number_of_nodes()
				# print 'G.number_of_edges():',G.number_of_edges()
				if had_Core:
					predict = calc_predict(Core)
		else: # predict			
			if u>v: u,v=v,u
			if had_Core:
				if (u,v) in predict: ans+=1
			else: newG.add_edge(u,v)	
			# if i==edgen: break		
		i+=1

	for u in G.nodes(): 
		G.node[u]['community'] = i
		i+=1 
	if not had_Core:
		NC = set()
		for u in Core:
			if u in newG and newG.degree(u)>=lb_train: NC.add(u)
		Core = NC
		pickle.dump(Core,open(file_name[:-4] + '--Core-all.txt','w'))
		if len(Core)>Core_num: Core = set(random.sample(Core, Core_num) )
		pickle.dump(Core,open(file_name[:-4] + '--Core.txt','w'))
	else:
		# Core_all = pickle.load(open(file_name[:-4] + '--Core-all.txt'))
		# G = G.subgraph(Core_all)
		pass
		# Core = pickle.load(open(file_name[:-4] + '--Core.txt'))
	# print 'Core size(before sample):', len(Core)
	
	# print 'Core size:', len(Core)
	# print 'newG.number_of_nodes():',newG.number_of_nodes()
	# print 'newG.number_of_edges():',newG.number_of_edges()
	# newG_E = sample_edges(newG)
	#calc_predict(Core)
	if had_Core and is_App:
		print ans,'/',e2
		ans = 1.0*ans/e2
		print 'Precision:', ans
		rp = RP(len(Core), e1,e2)
		print 'Random precision:', rp
		if ans: print 'Relative precision:', ans/rp
	# calc_distribution(G, newG)
	# MyPredict()
	
	print ('Total time:',time.time()-start_time)

if __name__ == '__main__':
	main()
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