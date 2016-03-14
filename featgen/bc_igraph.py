import igraph
import csv


import sys

if __name__=='__main__':

	input_file=sys.argv[1]
	output_file=sys.argv[2]
	g=igraph.Graph.Read_Ncol(input_file)
	g.summary()

	print igraph.summary(g)
	estimate = g.betweenness()

	with open(output_file, 'wb') as fout:
		outcsv = csv.writer(fout)
		for v in g.vs:
			outcsv.writerow([v["name"], estimate[v.index]])

