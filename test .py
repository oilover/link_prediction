import numba, matplotlib
import networkx as nx
file_name = 'facebook-wosn-links/facebook-wosn-links.txt' 

@numba.jit
def main():
	G = nx.Graph()
	G.add_path([0,1,2])
	G.add_path([0,10,2])
	# print nx.all_shortest_paths(G,0,2)
	nx.draw(G)

if __name__ == '__main__':
	main()