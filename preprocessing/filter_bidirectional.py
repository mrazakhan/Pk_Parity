import graphlab
import csv
import argparse
import graphlab.aggregate as agg
from collections import Counter
from graphlab import degree_counting

''' Assumption
Index,TowerId,Lat,Lng,District
District file has the header having TowerId and District

'''

DEBUG =1
def swapColNames(sf, ColA, ColB):
	sf.rename({ColA:'Temp'})
	sf.rename({ColB:ColA})
	sf.rename({'Temp':ColB})
	return sf

def filter_reciprocal_edges(input_file,callerIdIndex,receiverIdIndex,typeIndex,callerCellIndex,receiverCellIndex, output_file, voiceOnly=False):
	orig_data=graphlab.SFrame.read_csv(input_file)
	header=orig_data.column_names()
	orig_data.rename({header[callerIdIndex]:'CallerId',header[receiverIdIndex]:'ReceiverId', header[typeIndex]:'Type'})
        orig_data.rename({header[callerCellIndex]:'CallerCell',header[receiverCellIndex]:'ReceiverCell'})
	
	if voiceOnly:
		print '************** Shape before filtering ***********', orig_data.shape
		orig_data=orig_data.filter_by('GSM','Type')
		print '************** Shape after filtering ***********', orig_data.shape
	#Ordering the data according to src id and dest id and then removing duplicates
	data=orig_data['CallerId','ReceiverId'].flat_map(['CallerId','ReceiverId'],lambda x: [[x['CallerId'],x['ReceiverId']] if x['CallerId']<x['ReceiverId'] else [x['CallerId'],x['ReceiverId']]], column_types=[int,int])

        '''
	data=data.unique()
	data2=data.copy()
	print 'Before swapping\n', data2.head(2)
	data2=swapColNames(data2, 'CallerId','ReceiverId')
	print 'After swapping CallerId and ReceiverId\n', data2.head(2)
	data2=swapColNames(data2,'CallerCell','ReceiverCell')
	print 'After swapping CallerCell and ReceiverCell\n', data2.head(2)
	
	data=data.append(data2)
        '''
	filteredColumns=data[['CallerId','ReceiverId']]
	filteredColumns=filteredColumns.groupby(['CallerId','ReceiverId'], operations={'count': agg.COUNT()})
	filteredColumns['reciprocal']=filteredColumns['count'].apply(lambda x:x%2) # Even count columns represent reciprocal edges
	filteredColumns=filteredColumns.filter_by(0,'reciprocal')

	final_sf=filteredColumns.join(orig_data,on=['CallerId','ReceiverId'], how='left')
	final_sf.export_csv(output_file,quote_level=csv.QUOTE_NONE)

if __name__=='__main__':
	parser=argparse.ArgumentParser(description='Filter Bidirectional Edges')

	parser.add_argument('-ic','--cdr_file',required=True,help='input cdr file')
	parser.add_argument('-ci','--callerid_index',required=True, help='CallerIdIndex'    )
	parser.add_argument('-ri','--receiverid_index',required=True, help='ReceiverIdIndex'    )
	parser.add_argument('-cci','--callercell_index',required=True, help='CallerIdIndex'    )
	parser.add_argument('-rci','--receivercell_index',required=True, help='ReceiverIdIndex'    )
	parser.add_argument('-ti','--type_index',required=True, help='TypeIndex For Filtering GSM'    )
	parser.add_argument('-f','--filterGSM',default=0, help='filter gsm only'    )
	parser.add_argument('-o','--output_file',required=True, help='output file')

	args=parser.parse_args()

	cdr_file=args.cdr_file

	out_file=args.output_file


	ci=int(args.callerid_index)
	ri=int(args.receiverid_index)
	cci=int(args.callercell_index)
	rci=int(args.receivercell_index)
	ti=int(args.type_index)
	voiceOnly=int(args.filterGSM)
	pre='NoFiltering-'
	if voiceOnly:
		pre='GSMFiltering-'
	filter_reciprocal_edges(cdr_file,ci,ri,ti,cci, rci, out_file,  voiceOnly=voiceOnly)
