import graphlab as gl
import csv
import argparse
import graphlab.aggregate as agg

def extract_femalesonly_alter(profile_file,sf_orig,callerIdCol,receiverIdCol):
    sf_gender=gl.SFrame.read_csv(profile_file,delimiter='\t')
    print sf_gender.head()
    sf_gender.rename({'msisdn':receiverIdCol})

    sf_gender=sf_gender[[receiverIdCol,'gend']]
    print sf_gender['gend'].sketch_summary()
    sf_gender=sf_gender.filter_by(0, 'gend')
    print 'Profile SF shape after filtering females only'
    sf3=sf_gender.join(sf_orig, on=receiverIdCol)
    return sf3

def degree_extraction(input_file,profile_file, callerIdCol, receiverIdCol, outputFile):
    sf=gl.SFrame.read_csv(input_file)
    sf2=sf.groupby(key_columns=callerIdCol,operations={'ReceiverIdList':agg.CONCAT(receiverIdCol)})
    sf2['Degree']=sf2['ReceiverIdList'].apply(lambda x:len(set(x)))
    sf2=sf2[[callerIdCol,'Degree']]
    sf2.export_csv(outputFile,quote_level=csv.QUOTE_NONE)
    
    sf_females=extract_femalesonly_alter(profile_file, sf,callerIdCol, receiverIdCol)
    sf2=sf_females.groupby(key_columns=callerIdCol,operations={'ReceiverIdList':agg.CONCAT(receiverIdCol)})
    sf2['Degree']=sf2['ReceiverIdList'].apply(lambda x:len(set(x)))
    sf2=sf2[[callerIdCol,'Degree']]
    sf2.export_csv('Females_Alter_'+outputFile,quote_level=csv.QUOTE_NONE)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='DegreeExractor')
    parser.add_argument('-if','--input_file',help='input cdr file', required=True)
    parser.add_argument('-pf','--profile_file',help='profile file', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerId Col Name', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverId Col Name', required=True)
    parser.add_argument('-of','--output_file',help='output file', required=True)

    args=parser.parse_args()

    degree_extraction(args.input_file,args.profile_file, args.callerIdCol, args.receiverIdCol,args.output_file)
