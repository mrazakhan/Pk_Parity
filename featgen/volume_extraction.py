import graphlab as gl
import csv
import argparse
import graphlab.aggregate as agg

def volume_extraction(input_file, callerIdCol, receiverIdCol, outputFile):
    sf=gl.SFrame.read_csv(input_file)
    sf2=sf.groupby(key_columns=callerIdCol,operations={'Count':agg.COUNT()})
    #sf2['Degree']=sf2['ReceiverIdList'].apply(lambda x:len(set(x)))
    sf2=sf2[[callerIdCol,'Count']]
    sf2.export_csv(outputFile,quote_level=csv.QUOTE_NONE)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='VolumeExractor')
    parser.add_argument('-if','--input_file',help='input cdr file', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerId Col Name', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverId Col Name', required=True)
    parser.add_argument('-of','--output_file',help='output file', required=True)

    args=parser.parse_args()

    volume_extraction(args.input_file, args.callerIdCol, args.receiverIdCol,args.output_file)
