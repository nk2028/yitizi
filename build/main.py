import json
import networkx as nx

G = nx.Graph()

with open('yitizi.csv') as f:
	next(f)  # skip header
	for line in f:
		k, vs = line.rstrip().split(',')
		for v in vs:
			G.add_edge(k, v)

d = {n: ''.join(G.neighbors(n)) for n in G.nodes()}

with open('yitizi.json', 'w') as f:
	json.dump(d, f, ensure_ascii=False, separators=(',\n', ':'))
