#encoding=utf-8
from time import *
import sys
file_name='digg' #'out.digg-friends' #1670 time=0
# start time: Sat Aug 06 21:22:50 2005 --- Wed Jul 08 14:00:05 2009

if __name__ == '__main__':
	i=0
	edges = [] 
	c = 0
	cnt = 0
	dist = []
	L=-1
	print strptime('Sat Aug 06 21:22:50 2005')
	for line in open(file_name):
		str=line[:-1].split('\t')
		i+=1
		x = int(str[2])
		if x==0 : continue			
		m = strptime(str[3]).tm_mon
		if m==L or L==-1:
			cnt+=1
		else:
			dist.append(cnt)
			# print dist
			cnt=1
		L=m
	print dist
		#edges.append(x)
	
	# fo = open('digg','w')
	# edges = sorted(edges, key=lambda x:x[2])
	# print edges[:7]
	# for e in edges:
	# 	fo.write('%d\t%d\t%d\t%s\n'%(e[0],e[1],e[2],ctime(e[2])))
	# fo.close()


# [2407, 2034, 1279, 1007, 1049, 1211, 1001, 3815, 2704, 2574, 4357, 6488, 5815, 4942, 4163, 4241, 6222, 9065, 7011, 7080, 7082, 8407, 7063, 6574, 7176, 20944, 35897, 47954, 28501, 37571, 51369, 56667, 52742, 51915, 68619, 93272, 68190, 74385, 81149, 67633, 75456, 97932, 84266, 102786, 101710, 132150, 150864]