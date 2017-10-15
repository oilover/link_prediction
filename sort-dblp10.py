#encoding=utf-8
#sort by timestamp, discard multiple edges, self loops\
#directed --> undirected
from time import *
import sys, gc
name =  'dblp_coauthor' #
file_name = name+'/out.'+name  #'out.digg-friends' #1670 time=0
output_file = name+'/'+name+'-02-08.txt' 
# start time: Sat Aug 06 21:22:50 2005 --- Wed Jul 08 14:00:05 2009
#file_name = 'a/a.txt'
if __name__ == '__main__':
	ST = time()
	print ctime(ST)
	i=0
	edges = [] 
	dist = []
	# print strptime('Sat Aug 06 21:22:50 2005')
	print file_name
	min_t, max_t = 1e10,0
	D = {}
	Set_t = set()
	with open(file_name) as fin:
		for line in fin:
			# print line
			str=line[:-1].split(' ')
			i+=1
			if i<10: print str
			if not str[0].isdigit(): continue		
			if not str[-1].split('\t')[-1].isdigit(): continue
			
			if (i<7): print str

			t = int(str[-1].split('\t')[-1])
			Set_t.add(t)
			if i<10: print 't=',t
			if t==0 : continue		
			y = strptime(ctime(t)).tm_year
			min_t = min(min_t, t)
			max_t = max(max_t, t)
			if i%60000==7: print('Radom timestamp:',ctime(t))
			if not (2002<=y and y<=2003):continue
			
			u,v = [int(x) for x in str[:2]]
			if i<10: print u,v,t
			if u>v: u,v=v,u
			if u==v: continue
			if (u,v) in D: D[(u,v)] = min(D[(u,v)],t)
			else: D[(u,v)] = t
			if len(D)<6: print D
		
	edges = D.items()
	del D
	gc.collect()
	fo = open(output_file,'w')
	edges = sorted(edges, key=lambda x:x[-1])
	print edges[:7]
	for e in edges:
		fo.write('%d\t%d\t%d\t%s\n'%(e[0][0],e[0][1],int(e[-1]),ctime(e[-1])))
	fo.close()
	print len(edges)
	print 'Time range:',len(Set_t)
	print Set_t
	print [ctime(z) for z in Set_t]
	# print ctime(min_t),'--',ctime(max_t)
	print 'Time:',time()-ST
# [2407, 2034, 1279, 1007, 1049, 1211, 1001, 3815, 2704, 2574, 4357, 6488, 5815, 4942, 4163, 4241, 6222, 9065, 7011, 7080, 7082, 8407, 7063, 6574, 7176, 20944, 35897, 47954, 28501, 37571, 51369, 56667, 52742, 51915, 68619, 93272, 68190, 74385, 81149, 67633, 75456, 97932, 84266, 102786, 101710, 132150, 150864]