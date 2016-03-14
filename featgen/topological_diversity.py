import graphlab as gl
import math
import argparse
import csv

# Read SF, Make A Copy, Transpose A and B

def topological_diversity(input_file, output_file, callerIdCol, receiverIdCol):

    sf1=gl.SFrame.read_csv(input_file)
    sf1.head()
    sf2=sf1.copy()
    sf2.head()
    sf2=sf2.rename({callerIdCol:'B1',receiverIdCol:'A1'})
    sf2.head()
    sf2=sf2.rename({'A1':callerIdCol,'B1':receiverIdCol})
    sf2.head()
    sf=sf1.append(sf2)
    sf1.shape
    sf2.shape
    sf.shape
    sf.head()
    sf=sf[[callerIdCol, receiverIdCol]]
    
    # calculate Total
    sf_overall=sf.groupby(callerIdCol,{'OverallTotal':gl.aggregate.COUNT()})
    sf_total=sf.groupby([callerIdCol,receiverIdCol],{'Total':gl.aggregate.COUNT()})
    sf_overall=sf_overall.join(sf_total, on=callerIdCol,how='outer')
    sf_merged=sf.join(sf_overall, how='inner', on=callerIdCol)
    sf_degree=sf.groupby([callerIdCol],{'Degree':gl.aggregate.COUNT_DISTINCT(receiverIdCol)})
    sf_merged2=sf_merged.join(sf_degree, how ='inner', on=callerIdCol)
    sf_merged2['VolumeProportion']=sf_merged2['Total']/sf_merged2['OverallTotal']
    sf_merged2['log_VolumeProportion']=sf_merged2['VolumeProportion'].apply(lambda x:math.log(x))
    sf_merged2['Product_Proportion_log_VolumeProportion']=sf_merged2['VolumeProportion']*sf_merged2['log_VolumeProportion']
    sf_numerator=sf_merged2.groupby(callerIdCol,{'topological_diversity_numerator':gl.aggregate.SUM('Product_Proportion_log_VolumeProportion')})
    sf_merged3=sf_merged2.join(sf_numerator, on=callerIdCol, how='inner')
    sf_merged3['topological_diversity_denominator']=sf_merged3['Degree'].apply(lambda x:math.log(x))
    sf_merged3['topological_diversity']=-sf_merged3['topological_diversity_numerator']/(sf_merged3['topological_diversity_denominator']+1.0)
    sf_merged3=sf_merged3[[callerIdCol,'topological_diversity']].unique()
    sf_merged3.export_csv(output_file,quote_level=csv.QUOTE_NONE)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Topological Diversity')
    parser.add_argument('-if','--input_file',help='Input File', required=True)
    parser.add_argument('-of','--output_file',help='Output File', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerIdCol', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverIdCol', required=True)

    args=parser.parse_args()
    topological_diversity(args.input_file, args.output_file, args.callerIdCol, args.receiverIdCol)
