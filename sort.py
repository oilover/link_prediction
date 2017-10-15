#encoding=utf-8
#sort by timestamp, discard multiple edges, self loops
from time import *
import sys
name = 'dblp_coauthor'
file_name = name+'/out.'+name  #'out.digg-friends' #1670 time=0
output_file = name+'/'+name+'-01-10.txt' 
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
	min_t, max_t = 1e18,0
	for line in open(file_name):
		# print line
		str=line[:-1].split(' ')
		if not str[0].isdigit(): continue
		
		if not str[-1].isdigit(): continue
		i+=1
		t = int(str[-1])
		if t==0 : continue		
		y = strptime(ctime(t)).tm_year
		min_t = min(min_t, t)
		max_t = max(max_t, t)
		continue
		if not (2001<=y and y<=2010):continue
		if i%100000==7: print(ctime(t))
		u,v = [int(x) for x in str[:2]]
		if u>v: u,v=v,u
		if u==v: continue
		e=[u,v,t]			
		edges.append(e)
		
	print len(edges)
	# fo = open(output_file,'w')
	# edges = sorted(edges, key=lambda x:x[2])
	# new_edges = []
	# S = set()
	# for x in edges:
	# 	if (x[0],x[1]) in S: continue
	# 	S.add((x[0],x[1]))
	# 	new_edges.append(x)
	# edges = new_edges
	# print edges[:7]
	# for e in edges:
	# 	fo.write('%d\t%d\t%d\t%s\n'%(e[0],e[1],int(e[2]),ctime(e[2])))
	# fo.close()
	print len(edges)
	print ctime(min_t),'--',ctime(max_t)
	print 'Time:',time()-ST
# [2407, 2034, 1279, 1007, 1049, 1211, 1001, 3815, 2704, 2574, 4357, 6488, 5815, 4942, 4163, 4241, 6222, 9065, 7011, 7080, 7082, 8407, 7063, 6574, 7176, 20944, 35897, 47954, 28501, 37571, 51369, 56667, 52742, 51915, 68619, 93272, 68190, 74385, 81149, 67633, 75456, 97932, 84266, 102786, 101710, 132150, 150864]