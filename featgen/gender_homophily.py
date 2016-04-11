import graphlab as gl
import math
import argparse
import csv

# Read SF, Make A Copy, Transpose A and B
def convert_to_undirected(input_file, callerIdCol, receiverIdCol):
    sf1=gl.SFrame.read_csv(input_file)
    sf2=sf1.copy()
    sf2=sf2.rename({callerIdCol:'B1',receiverIdCol:'A1'})
    sf2=sf2.rename({'A1':callerIdCol,'B1':receiverIdCol})
    sf=sf1.append(sf2)
    return sf

def gender_homophily(sf,input_file,profile_file, output_file, callerIdCol, receiverIdCol):

    sf_gender=gl.SFrame.read_csv(profile_file,delimiter='\t')
    sf_gender.rename({'msisdn':receiverIdCol,'gend':'gender'})
    sf_merged=sf.join(sf_gender, how='inner', on=receiverIdCol)
    sf_merged.rename({'gender':'BPartyGender'})
    sf_gender.rename({receiverIdCol:callerIdCol})
    sf_merged=sf_merged.join(sf_gender, how='inner', on=callerIdCol)
    sf_merged.rename({'gender':'APartyGender'})

    sf_merged['SameGenderCall']=sf_merged['APartyGender','BPartyGender'].apply(lambda x:1 if x['APartyGender']==x['BPartyGender'] else 0)
    sf_total=sf_merged.groupby(callerIdCol,operations={'TotalCalls':gl.aggregate.COUNT(receiverIdCol), 'UniqueBParty':gl.aggregate.COUNT_DISTINCT(receiverIdCol)})
    sf_same=sf_merged.filter_by(1,'SameGenderCall').groupby(callerIdCol,operations={'TotalCalls_Same':gl.aggregate.COUNT(receiverIdCol), 'UniqueBParty_Same':gl.aggregate.COUNT_DISTINCT(receiverIdCol)})
    sf_merged=sf_total.join(sf_same, on=callerIdCol, how='left').fillna('TotalCalls_Same',0).fillna('UniqueBParty_Same',0)
    sf_merged['homophily_calls']=sf_merged['TotalCalls_Same']/sf_merged['TotalCalls']
    sf_merged['homophily_net']=sf_merged['UniqueBParty_Same']/sf_merged['UniqueBParty']
    sf_merged.export_csv(output_file,quote_level=csv.QUOTE_NONE)

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


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Topological Diversity')
    parser.add_argument('-if','--input_file',help='Input File', required=True)
    parser.add_argument('-pf','--profile_file',help='Profile File', required=True)
    parser.add_argument('-of','--output_file',help='Output File', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerIdCol', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverIdCol', required=True)

    args=parser.parse_args()
    sf_orig=convert_to_undirected(args.input_file,args.callerIdCol, args.receiverIdCol)    
    gender_homophily(sf_orig,args.input_file,args.profile_file, args.output_file, args.callerIdCol, args.receiverIdCol)
    sf_females=extract_femalesonly_alter(args.profile_file, sf_orig, args.callerIdCol, args.receiverIdCol)
    gender_homophily(sf_orig,args.input_file,args.profile_file, 'Females_Alter_'+args.output_file, args.callerIdCol, args.receiverIdCol)

