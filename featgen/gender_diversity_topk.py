import graphlab as gl
import math
import argparse
import csv

def topk(x,k=4):
	max_length=max(k,len(x))
	lst=[str(each[0]) for each in x[:max_length]]
	return lst

def filter_topfriends(sf, k=4):
    sf2=sf.groupby(['CallerId','ReceiverId'], operations={'count':gl.aggregate.COUNT()})
    sf2=sf2.groupby('CallerId',operations={'FriendsList':gl.aggregate.CONCAT('ReceiverId','count')})
    sf2['FriendsList']=sf2['FriendsList'].apply(lambda d:sorted(d.items(), key=lambda x: -x[1]))

    sf2['FriendsList']=sf2['FriendsList'].apply(lambda x:topk(x,k))
    sf=sf2.stack('FriendsList','ReceiverId')
    return sf

# Read SF, Make A Copy, Transpose A and B

def gender_diversity(input_file,profile_file, output_file, callerIdCol, receiverIdCol):
    sf1=gl.SFrame.read_csv(input_file, column_type_hints=str)
    sf1.head()
    sf2=sf1.copy()
    sf2.head()
    sf2=sf2.rename({callerIdCol:'B1',receiverIdCol:'A1'})
    sf2.head()
    sf2=sf2.rename({'A1':callerIdCol,'B1':receiverIdCol})
    sf2.head()
    sf_orig=sf1.append(sf2)
    for k in [2,4]:
        sf=filter_topfriends(sf_orig, k=k)
        sf_gender=gl.SFrame.read_csv(profile_file,delimiter='\t', column_type_hints=str)
        sf_gender.rename({'msisdn':receiverIdCol})
        sf_merged=sf.join(sf_gender, how='inner', on=receiverIdCol)
        sf_merged=sf.join(sf_gender, how='inner', on=receiverIdCol)
        sf_gender_overall=sf_merged.groupby([callerIdCol,'gend'],{'GenderTotal':gl.aggregate.COUNT()})
        sf_total=sf_merged.groupby(callerIdCol,{'OverallTotal':gl.aggregate.COUNT(),'UniqueBPartyGender':gl.aggregate.COUNT_DISTINCT('gend')})
        sf_final=sf_gender_overall.join(sf_total,on=callerIdCol, how='inner')
        sf_final['VolumeProportion']=sf_final['GenderTotal']/sf_final['OverallTotal']
        sf_final['log_VolumeProportion']=sf_final['VolumeProportion'].apply(lambda x:math.log(x))
        sf_final['Product_Proportion_log_VolumeProportion']=-sf_final['VolumeProportion']*sf_final['log_VolumeProportion']
        sf_numerator=sf_final.groupby(callerIdCol,{'gender_diversity_numerator':gl.aggregate.SUM('Product_Proportion_log_VolumeProportion')})
        sf_gender_diversity=sf_final.join(sf_numerator,on=callerIdCol, how='inner')[[callerIdCol,'gender_diversity_numerator','UniqueBPartyGender']]
        sf_gender_diversity['denominator']=sf_gender_diversity['UniqueBPartyGender'].apply(lambda x:math.log(x))
        sf_gender_diversity['gender_diversity']=sf_gender_diversity['gender_diversity_numerator']/(sf_gender_diversity['denominator']+1.0)
        sf_gender_diversity=sf_gender_diversity.unique()
        sf_gender_diversity.export_csv('Top'+str(k)+'_'+output_file,quote_level=csv.QUOTE_NONE)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Topological Diversity')
    parser.add_argument('-if','--input_file',help='Input File', required=True)
    parser.add_argument('-pf','--profile_file',help='Profile File', required=True)
    parser.add_argument('-of','--output_file',help='Output File', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerIdCol', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverIdCol', required=True)

    args=parser.parse_args()
    gender_diversity(args.input_file,args.profile_file, args.output_file, args.callerIdCol, args.receiverIdCol)
