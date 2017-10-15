
import random
start_line=5
file_name='com-dblp.ungraph.txt'
output = 'dblp-random.txt'
if __name__ == '__main__':
	print ('1	2'.split('\t'))
	i=1
	edges = []
	for line in open(file_name):
		if i>=start_line:
			# if i<10: print line.strip('\t')
			e = [int(x) for x in line.split('\t')]
			edges.append(e)
		i+=1
	random.shuffle(edges)
	print edges[:10]
	f = open(output,'w')
	for e in edges:
		f.write('%d\t%d\n' % (e[0],e[1]))