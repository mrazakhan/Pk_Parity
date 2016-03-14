from collections import defaultdict
import snap
import sys

#filename='Df_UniqueEdgeList_0602_Kigali.csv'
def loadGraph(filename):
	G1 = snap.TUNGraph.New()
	count=0
	with open(filename,'r') as fin:
		for each in fin:
			if 'CallerId' not in each:
					srcId,destId=each.strip().split(',')[:2]
					srcId=int(srcId.strip())
					destId=int(destId.strip())
					print srcId, destId
					if not G1.IsNode(srcId):
						G1.AddNode(srcId)
					if not G1.IsNode(destId):
						G1.AddNode(destId)
					G1.AddEdge(srcId, destId)
					count+=1	

	print 'Graph loading complete, No of Edges', count		
	return G1
	
'''return support nodes dict and degree dict	'''
def get_betweennesscentrality(G1):	
	Nodes = snap.TIntFltH()
	Edges = snap.TIntPrFltH()
	snap.GetBetweennessCentr(UGraph, Nodes, Edges, 1.0)
	return Nodes
def write_output(filename, nodes_dict):	
	# Format 
	## Subscriber, Degree, Support Nodes Count, Support Nodes List
	
	with open(filename,'w') as fout:
		for node in nodes_dict:	
			fout.write(str(node)+','+str(nodes_dict[node])+'\n')

			
if __name__=='__main__':
	if len(sys.argv)!=3:
		print 'Wrong Number of Arguments'
		print 'Required Arguments: inputfilename, outputfile'
		sys.exit(-1)
		
	inputfilename=sys.argv[1]
	outputfilename=sys.argv[2]
	
	G1=loadGraph(inputfilename)
	nodes_dict=get_betweennesscentrality(G1)
	write_output(outputfilename,nodes_dict )
