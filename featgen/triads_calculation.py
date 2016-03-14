import graphlab
import csv
import argparse
import graphlab.aggregate as agg
from graphlab import degree_counting

def triads_calculation(input_file, callerIdCol, receiverIdCol, outputFile):

	data=graphlab.SFrame.read_csv(input_file, delimiter=',')
	data.rename({callerIdCol:'__src_id',receiverIdCol:'__dst_id'})

	# Ordering the data according to src id and dest id and then removing duplicates
	data=data['__src_id','__dst_id'].flat_map(['__src_id','__dst_id'],lambda x: [[x['__src_id'],x['__dst_id']] if x['__src_id']<x['__dst_id'] else [x['__dst_id'],x['__src_id']]])

	data=data.unique()

	g1=graphlab.SGraph(edges=data)
	#data=graphlab.SFrame.read_csv(input_file, header=False, delimiter=',')
	
	#g1=graphlab.load_sgraph(input_file, format='csv')
	tc = graphlab.triangle_counting.create(g1)
	g1.vertices['triangle_count'] = tc['graph'].vertices['triangle_count']

	deg = degree_counting.create(g1)

	g1.vertices['total_degree'] = deg['graph'].vertices['total_degree']

	g1.vertices['embeddedness']=g1.vertices['triangle_count']/(0.5*g1.vertices['total_degree']*(g1.vertices['total_degree']-1)+1)

	g1.vertices['SubscriberId'] = g1.vertices['__id']

	g1.vertices.save(outputFile, format='csv')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='DegreeExractor')
    parser.add_argument('-if','--input_file',help='input cdr file', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerId Col Name', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverId Col Name', required=True)
    parser.add_argument('-of','--output_file',help='output file', required=True)

    args=parser.parse_args()

    triads_calculation(args.input_file, args.callerIdCol, args.receiverIdCol,args.output_file)
