'''
	Digg: need to be sorted by timestamps (279,630 nodes and 1,731,653 directed edges) 170w
	wiki-growth: 1,870,709 nodes and 39,953,145 directed edges
'''
from __future__ import print_function
import sys,time
import networkx as nx
from random import random,shuffle
import numba

file_name = 'digg-friends/digg-friends.txt' 
output_file = file_name[:-4] + '-output-App.txt'
noden, edgen = 317080 , 1546540#335708 # 104824 #1500000 #33140018
predict = {}
train_p = 0.5
Core_num = 500
lb_train = 3
K = 50
H = [{} for i in range(K)]
h = [{} for i in range(K)]
I = [{} for i in range(K)]

def App_Ja(u,v):
	cnt=0
	for i in range(K): 
		if u in I[i] and I[i][u]==I[i][v]: cnt+=1
	return 1.0*cnt/K

@numba.jit
def get_predict(G, Core):
	print ('Begin predict...')
	predict = {}
	num = 0;
	for u in Core:
		# if not u in newG.nodes(): continue;
		for v in set(G[u].keys()):
			# if not v in newG.nodes(): continue;
			for U in set(G[v].keys())&Core - set(G[u].keys()):
				if u>=U: continue
				if (u,U) in predict: continue
				num+=1
				s = App_Ja(u,U)
				if (s>=0.14):
					predict[(u,U)]= s
	print ('Predict complexity:',num)
	print ('len(predict):', len(predict))
	return predict

@numba.jit
def update(u,v):
	pass
	# for k in range(K):
	# 	if not u in h[k]: h[k][u] = random()
	# 	if not v in h[k]: h[k][v] = random()
	# 	if not u in H[k] or h[k][v]<H[k][u]: 
	# 		H[k][u] = h[k][v]
	# 		I[k][u] = v
	# 	if not v in H[k] or h[k][u]<H[k][v]:
	# 		H[k][v] = h[k][u]
	# 		I[k][v] = u

# @numba.jit
had_Core = True
def main():
	start_time = time.time()
	print time.ctime(start_time)
	edgen_new = 0;
	i=1;
	G = nx.Graph()
	newG = nx.Graph()
	train_edge_num = int(edgen*train_p)
	print ('Data: ',file_name)
	print ('train_edge_num:',train_edge_num)
	fo = open(output_file,'w')
	if had_Core:
		Core = pickle.load(open(file_name[:-4] + '--Core.txt'))
	for line in open(file_name):
		str = line.split('\t')
		u,v=[int(x) for x in str[:2]]
		if G.has_edge(u,v): print ('Multiple edge')
		# if u>v: u,v=v,u
		if i<=train_edge_num:
			G.add_edge(u,v)
			if not had_Core:
				if G.degree(u)==lb_train: Core.add(u)
				if G.degree(v)==lb_train: Core.add(v)
			if had_Core and (u in Core or v in Core):
				update(u,v)
			if i==train_edge_num:
				fo.write('Begin training..G node:%d'%(G.number_of_nodes()))
				fo.flush()
				Core = G.nodes()
	
				shuffle(Core)
				Core = set(Core[:Core_num])
				print ('G.number_of_nodes():',G.number_of_nodes())
				print ('G.number_of_edges():',G.number_of_edges())
				predict = get_predict(G, Core)
				G = G.subgraph(Core)
				print ('Core subgraph of G:')
				print ('G.number_of_nodes():',G.number_of_nodes())
				print ('G.number_of_edges():',G.number_of_edges())
		else: # predict
			if (not u in Core) or (not v in Core):
				continue;
			edgen_new+=1;
			if i%10==0 and (u,v) in predict:
				fo.write("%d (%d,%d) %.3f\n"%(i,u,v,predict[(u,v)]))
			if i%1000==0: fo.flush()
			newG.add_edge(u,v)	
			if i==edgen: break		
		i+=1
	
	
	fo.close();
	prediction = sorted(predict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)  #key=lambda x:x[1]
	edgen_new = newG.number_of_edges()
#	assert 
	
	print ('newG.number_of_nodes():',newG.number_of_nodes())
	print ('newG.number_of_edges():',newG.number_of_edges())
#	s = input('Enter to continue..')
	prediction = prediction[:edgen_new]
	print (prediction[:10])
	ans = 0
	for x in prediction:
		u,v=x[0]
		if newG.has_edge(u,v):
			ans+=1
	ans = 1.0*ans/newG.number_of_edges()
	print ('Precision:', ans)
	N = len(Core)
	C = N*(N-1)/2 - G.number_of_edges();
	print ('Random precision:', newG.number_of_edges()*1.0/C)
	print ('Relative precision:', ans*C/newG.number_of_edges() )
	print('Total time:',time.time()-start_time)

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
# train_edge_num: 454982
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

# facebook-sorted  		train_edge_num: 454982
# Begin predict...
# Predict complexity: 6288
# newG.number_of_nodes(): 859
# newG.number_of_edges(): 715
# [((32990, 34886), 0.6), ((28385, 45502), 0.56), ((23442, 34886), 0.54), ((6825, 6832), 0.5), ((3152, 3164), 0.5), ((1004, 1005), 0.48), ((23899, 23901), 0.48), ((28075, 32311), 0.46), ((22047, 32276), 0.44), ((20739, 31545), 0.42)]
# Precision: 0.0615384615385
# Random precision: 9.71534534109e-07
# Relative precision: 63341.5070468
# [Finished in 108.1s]

# Data:  facebook-sorted.txt
# train_edge_num: 454982
# Begin predict...
# Predict complexity: 52636
# newG.number_of_nodes(): 829
# newG.number_of_edges(): 730
# [((13433, 52992), 1.0), ((43936, 43939), 1.0), ((60513, 60517), 1.0), ((53032, 55164), 1.0), ((60515, 60517), 1.0), ((54287, 54288), 1.0), ((60513, 60515), 1.0), ((51884, 54685), 1.0), ((25176, 40937), 0.88), ((16004, 16009), 0.72)]
# Precision: 0.0561643835616
# Random precision: 0.0001623486738
# Relative precision: 345.949136799
# [Finished in 91.3s]