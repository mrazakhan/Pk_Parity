import graphlab as gl
import math
import argparse
import csv

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

def convert_to_undirected(input_file, callerIdCol, receiverIdCol):
    sf1=gl.SFrame.read_csv(input_file)
    sf2=sf1.copy()
    sf2=sf2.rename({callerIdCol:'B1',receiverIdCol:'A1'})
    sf2=sf2.rename({'A1':callerIdCol,'B1':receiverIdCol})
    sf=sf1.append(sf2)
    return sf

# Read SF, Make A Copy, Transpose A and B

def gender_diversity(sf,input_file,profile_file, output_file, callerIdCol, receiverIdCol):

    sf_gender=gl.SFrame.read_csv(profile_file,delimiter='\t')
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
    sf_gender_diversity.export_csv(output_file,quote_level=csv.QUOTE_NONE)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Topological Diversity')
    parser.add_argument('-if','--input_file',help='Input File', required=True)
    parser.add_argument('-pf','--profile_file',help='Profile File', required=True)
    parser.add_argument('-of','--output_file',help='Output File', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerIdCol', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverIdCol', required=True)

    args=parser.parse_args()
    sf_undirected=convert_to_undirected(args.input_file, args.callerIdCol, args.receiverIdCol)
    gender_diversity(sf_undirected,args.input_file,args.profile_file, args.output_file, args.callerIdCol, args.receiverIdCol)
    sf_females=extract_femalesonly_alter(args.profile_file,sf_undirected,args.callerIdCol,args.receiverIdCol)
    gender_diversity(sf_females,args.input_file,args.profile_file, 'Females_Alter_'+args.output_file, args.callerIdCol, args.receiverIdCol)
