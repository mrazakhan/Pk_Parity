"""
Example of parallel implementation of betweenness centrality using the
multiprocessing module from Python Standard Library.

The function betweenness centrality accepts a bunch of nodes and computes
the contribution of those nodes to the betweenness centrality of the whole
network. Here we divide the network in chunks of nodes and we compute their
contribution to the betweenness centrality of the whole network.
"""

from multiprocessing import Pool
import time
import itertools
import networkx as nx
import pandas as pd
import sys
def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x


def _betmap(G_normalized_weight_sources_tuple):
    """Pool for multiprocess only accepts functions with one argument.
    This function uses a tuple as its only argument. We use a named tuple for
    python 3 compatibility, and then unpack it when we send it to
    `betweenness_centrality_source`
    """
    return nx.betweenness_centrality_source(*G_normalized_weight_sources_tuple)


def betweenness_centrality_parallel(G, processes=None):
    """Parallel betweenness centrality  function"""
    p = Pool(processes=processes)
    node_divisor = len(p._pool)*8
    node_chunks = list(chunks(G.nodes(), int(G.order()/node_divisor)))
    num_chunks = len(node_chunks)
    bt_sc = p.map(_betmap,
                  zip([G]*num_chunks,
                      [True]*num_chunks,
                      [None]*num_chunks,
                      node_chunks))

    # Reduce the partial solutions
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return bt_c

if __name__ == "__main__":
	input_file=sys.argv[1]
	output_file=sys.argv[2]
	df=pd.read_csv(input_file)
	G_ba = nx.from_pandas_dataframe(df, 'CallerId', 'ReceiverId')
    #G_er = nx.gnp_random_graph(1000, 0.01)
    #G_ws = nx.connected_watts_strogatz_graph(1000, 4, 0.1)
	for G in [G_ba]:
		print("")
		print("Computing betweenness centrality for:")
		print(nx.info(G))
		print("\tParallel version")
		start = time.time()
		bt = betweenness_centrality_parallel(G)
		with open(output_file) as fout:
			for each in bt:
				fout.write(each+','+bt[each]+'\n')    
