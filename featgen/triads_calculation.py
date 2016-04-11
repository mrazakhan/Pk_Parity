import graphlab
import csv
import argparse
import graphlab.aggregate as agg
from graphlab import degree_counting


def convert_to_undirected(input_file, callerIdCol, receiverIdCol):
    sf1=graphlab.SFrame.read_csv(input_file)
    sf2=sf1.copy()
    sf2=sf2.rename({callerIdCol:'B1',receiverIdCol:'A1'})
    sf2=sf2.rename({'A1':callerIdCol,'B1':receiverIdCol})
    sf=sf1.append(sf2)
    return sf

def extract_femalesonly_alter(profile_file,sf_orig,callerIdCol,receiverIdCol):
    sf_gender=graphlab.SFrame.read_csv(profile_file,delimiter='\t')
    print sf_gender.head()
    sf_gender.rename({'msisdn':receiverIdCol})
    sf_gender=sf_gender[[receiverIdCol,'gend']]
    print sf_gender['gend'].sketch_summary()
    sf_gender=sf_gender.filter_by(0, 'gend')
    print 'Profile SF shape after filtering females only'
    sf3=sf_gender.join(sf_orig, on=receiverIdCol)
    return sf3


def triads_calculation(data,input_file, callerIdCol, receiverIdCol, outputFile):

	#data=graphlab.SFrame.read_csv(input_file, delimiter=',')
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
    parser.add_argument('-pf','--profile_file',help='profile file', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerId Col Name', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverId Col Name', required=True)
    parser.add_argument('-of','--output_file',help='output file', required=True)

    args=parser.parse_args()
    data=convert_to_undirected(args.input_file,args.callerIdCol, args.receiverIdCol)
    print '**************************'
    print data.head()
    triads_calculation(data,args.input_file, args.callerIdCol, args.receiverIdCol,args.output_file)
    female_sf=extract_femalesonly_alter(args.profile_file,data,args.callerIdCol,args.receiverIdCol)
    triads_calculation(female_sf,args.input_file, args.callerIdCol, args.receiverIdCol,'Females_Alter_'+args.output_file)

