'''
This code filters out the users either on the basis of their profile information ( For example, only one account per cnic ) or
the activity information ( people having very high degree)
'''
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

def filter(input_file,callerIdIndex,receiverIdIndex,filter_file,filterCallerIdIndex, output_file, type_index=0, filter_GSM=0):
        filter_data=graphlab.SFrame.read_csv(filter_file, column_type_hints=str)
        filter_header=filter_data.column_names()
	orig_data=graphlab.SFrame.read_csv(input_file, column_type_hints=str)
	header=orig_data.column_names()

        if 'CallerId' not in header:
	    orig_data.rename({header[callerIdIndex]:'CallerId'})
        if 'ReceiverId' not in header:
	    orig_data.rename({header[receiverIdIndex]:'ReceiverId'})
        
        if filter_GSM!=0:
            if 'Type' not in header:
                orig_data.rename({header[type_index]:'Type'})
            print 'Shape before filtering GSM', orig_data.shape
            orig_data=orig_data.filter_by('GSM','Type')
            print 'Shape after filtering GSM', orig_data.shape
	
        filter_data.rename({filter_header[filterCallerIdIndex]:'CallerId'})

        
        # Filter orig_data by filter_data
        filtered_data=orig_data.filter_by(filter_data['CallerId'],'CallerId')
        print filtered_data.head() 
        print 'Shape of the filtered data after filtering on the basis of Caller Id', filtered_data.shape
        filtered_data=filtered_data.filter_by(filter_data['CallerId'],'ReceiverId') 
        print 'Shape of the filtered data after filtering on the basis of Reciver Id', filtered_data.shape

        filtered_data.export_csv(output_file, quote_level=csv.QUOTE_NONE)


if __name__=='__main__':
	parser=argparse.ArgumentParser(description='Filter Bidirectional Edges')

	parser.add_argument('-ic','--cdr_file',required=True,help='input cdr file')
	parser.add_argument('-ci','--callerid_index',required=True, help='CallerIdIndex'    )
	parser.add_argument('-ri','--receiverid_index',required=True, help='ReceiverIdIndex'    )
	parser.add_argument('-ti','--type_index',required=False, help='ReceiverIdIndex'    )
        parser.add_argument('-f','--filterGSM',default=0, help='filter gsm only'    )
        parser.add_argument('-if','--filter_file',required=True,help='input filter file')
	parser.add_argument('-fci','--filter_callerid_index',required=True, help='CallerIdIndex in the filter file'    )
	parser.add_argument('-o','--output_file',required=True, help='output file')

	args=parser.parse_args()

	cdr_file=args.cdr_file
        filter_file=args.filter_file
	out_file=args.output_file


	ci=int(args.callerid_index)
	ri=int(args.receiverid_index)
	fci=int(args.filter_callerid_index)
        ti=0
        filter_GSM=0
        if args.filterGSM!=0:
            ti=int(args.type_index)
            filter_GSM=1
	filter(cdr_file,ci,ri,filter_file,fci, out_file, type_index=ti, filter_GSM=filter_GSM)
