import graphlab as gl
import math
import argparse
import csv

def convert_to_undirected(input_file, callerIdCol, receiverIdCol):
    sf1=gl.SFrame.read_csv(input_file)
    sf2=sf1.copy()
    sf2=sf2.rename({callerIdCol:'B1',receiverIdCol:'A1'})
    sf2=sf2.rename({'A1':callerIdCol,'B1':receiverIdCol})
    sf=sf1.append(sf2)
    return sf

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


# Read SF, Make A Copy, Transpose A and B

def topological_diversity(sf,input_file, output_file, callerIdCol, receiverIdCol):

    sf=sf[[callerIdCol, receiverIdCol]]
    
    # calculate Total
    sf_overall=sf.groupby(callerIdCol,{'OverallTotal':gl.aggregate.COUNT()})
    sf_total=sf.groupby([callerIdCol,receiverIdCol],{'Total':gl.aggregate.COUNT()})
    sf_overall=sf_overall.join(sf_total, on=callerIdCol,how='outer')
    sf_merged=sf.join(sf_overall, how='inner', on=callerIdCol)
    sf_degree=sf.groupby([callerIdCol],{'Degree':gl.aggregate.COUNT_DISTINCT(receiverIdCol)})
    sf_merged2=sf_overall.join(sf_degree, how ='inner', on=callerIdCol)
    #sf_merged2=sf_merged.join(sf_degree, how ='inner', on=callerIdCol)
    sf_merged2['VolumeProportion']=sf_merged2['Total']/sf_merged2['OverallTotal']
    sf_merged2['log_VolumeProportion']=sf_merged2['VolumeProportion'].apply(lambda x:math.log(x))
    sf_merged2['Product_Proportion_log_VolumeProportion']=-sf_merged2['VolumeProportion']*sf_merged2['log_VolumeProportion']
    sf_numerator=sf_merged2.groupby(callerIdCol,{'topological_diversity_numerator':gl.aggregate.SUM('Product_Proportion_log_VolumeProportion')})
    sf_merged3=sf_merged2.join(sf_numerator, on=callerIdCol, how='inner')
    sf_merged3['topological_diversity_denominator']=sf_merged3['Degree'].apply(lambda x:math.log(x))
    sf_merged3['topological_diversity']=sf_merged3['topological_diversity_numerator']/(sf_merged3['topological_diversity_denominator']+1.0)
    sf_merged3=sf_merged3[[callerIdCol,'topological_diversity']].unique()
    sf_merged3.export_csv(output_file,quote_level=csv.QUOTE_NONE)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Topological Diversity')
    parser.add_argument('-if','--input_file',help='Input File', required=True)
    parser.add_argument('-pf','--profile_file',help='Profile File', required=True)
    parser.add_argument('-of','--output_file',help='Output File', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerIdCol', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverIdCol', required=True)

    args=parser.parse_args()
    sf_undirected=convert_to_undirected(args.input_file, args.callerIdCol, args.receiverIdCol)
    topological_diversity(sf_undirected,args.input_file, args.output_file, args.callerIdCol, args.receiverIdCol)
    sf_females=extract_femalesonly_alter(args.profile_file,sf_undirected,args.callerIdCol,args.receiverIdCol)
    topological_diversity(sf_females,args.input_file, 'Females_Alter_'+args.output_file, args.callerIdCol, args.receiverIdCol)
