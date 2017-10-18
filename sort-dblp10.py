#encoding=utf-8
#sort by timestamp, discard multiple edges, self loops\
#directed --> undirected
from time import *
import sys, gc, re
name =  'dblp_coauthor' #
file_name = name+'/out.'+name  #'out.digg-friends' #1670 time=0
output_file = name+'/'+name+'-01-08.txt' 
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
			str=re.split(' |\t', line[:-1]) 
			i+=1
			if i<10: print str
			if not str[0].isdigit(): continue		
			if not str[-1].isdigit(): continue
			
			if (i<7): print str

			t = ctime(int(str[-1]))			
			y = strptime(t).tm_year	
			t = y
			Set_t.add(t)			
			if not ( y<=2008):continue
			
			u,v = [int(x) for x in str[:2]]
			if u>v: u,v=v,u
			if u==v: continue
			if (u,v) in D: D[(u,v)] = min(D[(u,v)],t)
			else: D[(u,v)] = t
			if len(D)<6: print D
		
	edges = D.items()
	del D
	gc.collect()
	print len(edges)
	fo = open(output_file,'w')
	
	edges.sort(key=lambda x:x[-1])
	print edges[:7]
	for e in edges:
		fo.write('%d\t%d\t%d\n'%(e[0][0],e[0][1],int(e[-1])))
	fo.close()
	
	print 'Time range:',len(Set_t)
	print Set_t
	print [ctime(z) for z in Set_t]
	# print ctime(min_t),'--',ctime(max_t)
	print 'Time:',time()-ST
# [2407, 2034, 1279, 1007, 1049, 1211, 1001, 3815, 2704, 2574, 4357, 6488, 5815, 4942, 4163, 4241, 6222, 9065, 7011, 7080, 7082, 8407, 7063, 6574, 7176, 20944, 35897, 47954, 28501, 37571, 51369, 56667, 52742, 51915, 68619, 93272, 68190, 74385, 81149, 67633, 75456, 97932, 84266, 102786, 101710, 132150, 150864]
['Wed Jan 01 08:01:01 2014', 'Fri Jan 01 08:01:01 2010', 'Sun Jan 01 08:01:01 1978', 'Sun Jan 01 08:01:01 2006', 'Tue Jan 01 08:01:01 2002', 'Thu Jan 01 08:01:01 1998', 'Sat Jan 01 08:01:01 1994', 'Sat Jan 01 08:01:01 1983', 'Mon Jan 01 08:01:01 1990', 'Sun Jan 01 08:01:01 2012', 'Wed Jan 01 08:01:01 1986', 'Sat Jan 01 08:01:01 2011', 'Mon Jan 01 08:01:01 2007', 'Wed Jan 01 08:01:01 2003', 'Fri Jan 01 08:01:01 1999', 'Wed Jan 01 08:01:01 1975', 'Sun Jan 01 08:01:01 1995', 'Tue Jan 01 08:01:01 1991', 'Tue Jan 01 08:01:01 1974', 'Thu Jan 01 08:01:01 1987', 'Fri Jan 01 08:01:01 1971', 'Mon Jan 01 08:01:01 1973', 'Tue Jan 01 08:01:01 2008', 'Mon Jan 01 08:01:01 1979', 'Thu Jan 01 08:01:01 2004', 'Sat Jan 01 08:01:01 2000', 'Mon Jan 01 08:01:01 1996', 'Wed Jan 01 08:01:01 1992', 'Fri Jan 01 08:01:01 1988', 'Fri Jan 01 08:01:01 1982', 'Tue Jan 01 08:01:01 1985', 'Sun Jan 01 08:01:01 1984', 'Tue Jan 01 08:01:01 1980', 'Thu Jan 01 08:01:01 1976', 'Thu Jan 01 08:01:01 1970', 'Thu Jan 01 08:01:01 1981', 'Sat Jan 01 08:01:01 1972', 'Thu Jan 01 08:01:01 2009', 'Sat Jan 01 08:01:01 2005', 'Thu Jan 01 08:15:57 1970', 'Tue Jan 01 08:01:01 2013', 'Sat Jan 01 08:01:01 1977', 'Mon Jan 01 08:01:01 2001', 'Wed Jan 01 08:01:01 1997', 'Fri Jan 01 08:01:01 1993', 'Sun Jan 01 08:01:01 1989']