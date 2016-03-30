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
					srcId,destId=each.strip().split(',')
					srcId=int(srcId[4:])
					destId=int(destId[4:])
					if not G1.IsNode(srcId):
						G1.AddNode(srcId)
					if not G1.IsNode(destId):
						G1.AddNode(destId)
					G1.AddEdge(srcId, destId)
					count+=1	

	print 'Graph loading complete, No of Edges', count		
	return G1
	
'''return support nodes dict and degree dict	'''
def get_support(G1):	
	support_nodes_dict=defaultdict(list)
	neighbors_distance1=defaultdict(list)
	neighbors_distance2=defaultdict(list)
	degree_subscribers=defaultdict(int)
	count=0
	for EI in G1.Edges():
		src=EI.GetSrcNId()
		dest=EI.GetDstNId()	
		for Id in G1.GetNI(src).GetOutEdges():
			if Id not in neighbors_distance1[src]:
				neighbors_distance1[src].append(Id)
			#if Id in G1.GetNI(dest).GetOutEdges():
			if Id not in neighbors_distance2[dest]:
				neighbors_distance2[dest].append(Id)
		for Id in G1.GetNI(dest).GetOutEdges():
			if Id not in neighbors_distance1[dest]:
				neighbors_distance1[dest].append(Id)
			#if Id in G1.GetNI(src).GetOutEdges():
			if Id not in neighbors_distance2[src]:
				neighbors_distance2[src].append(Id)
		count+=1
		if count%10000==0:
			print 'Edges Traversed', count
		
	
	for node in neighbors_distance1:
		#Intersection of distance1 neighbors and distance2 neighbors will give us the support
		support_nodes_dict[node]=list(set(neighbors_distance1[node])&set(neighbors_distance2[node]))
		degree_subscribers[node]=len(set(neighbors_distance1[node]))
	return support_nodes_dict,degree_subscribers

def write_output(filename, support_nodes_dict, degree_dict):	
	# Format 
	## Subscriber, Degree, Support Nodes Count, Support Nodes List
	
	with open(filename,'w') as fout:
		fout.write('SubscriberId,Degree,SupportCount,SupportNodes\n')
		for node in support_nodes_dict:	
			fout.write('1046'+str(node).zfill(8)+','+str(degree_dict[node])+','+str(len(support_nodes_dict[node]))+','+'_'.join('1046'+str(each).zfill(8) for each in support_nodes_dict[node])+'\n')

			
if __name__=='__main__':
	if len(sys.argv)!=3:
		print 'Wrong Number of Arguments'
		print 'Required Arguments: inputfilename, outputfile'
		sys.exit(-1)
		
	inputfilename=sys.argv[1]
	outputfilename=sys.argv[2]
	
	G1=loadGraph(inputfilename)
	support_dict, degree_dict=get_support(G1)
	write_output(outputfilename,support_dict, degree_dict )
