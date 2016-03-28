import graphlab as gl
import math
import argparse
import csv
import sys
# Read SF, Make A Copy, Transpose A and B

def location_diversity(input_file, output_file, callerIdCol, receiverIdCol, callerCellCol, receiverCellCol):

    sf1=gl.SFrame.read_csv(input_file)
    sf1.head()
    sf2=sf1.copy()
    sf2.head()
    sf2=sf2.rename({callerIdCol:'B1',receiverIdCol:'A1'})
    sf2=sf2.rename({callerCellCol:'B1Cell',receiverCellCol:'A1Cell'})
    sf2=sf2.rename({'A1':callerIdCol,'B1':receiverIdCol})
    sf2=sf2.rename({'A1Cell':callerCellCol,'B1Cell':receiverCellCol})
    sf2.head()
    sf=sf1.append(sf2)
    sf1.shape
    sf2.shape
    sf.shape
    sf.head()
    sf=sf[[callerIdCol, callerCellCol]].dropna()
    sf.rename({callerCellCol:'Loc'})
    print 'Shape before filtering missing towers', sf.shape
    sf1=sf.filter_by('', 'Loc', exclude=True)
    print 'Shape after filtering missing towers', sf.shape
    
    
    # calculate Total
    sf=sf1.groupby([callerIdCol,'Loc'],{'LocTotal':gl.aggregate.COUNT()})
    sf_total=sf1.groupby([callerIdCol],{'OverallTotal':gl.aggregate.COUNT()})
    sf_final=sf.join(sf_total,on=callerIdCol, how='inner')
    sf_final['VolumeProportion']=sf_final['LocTotal']/sf_final['OverallTotal']
    print sf_final['VolumeProportion'].sketch_summary()
    sf_final.export_csv('Location_Diversity_Debug.csv')
    #sys.exit(0)
    sf_final['log_VolumeProportion']=sf_final['VolumeProportion'].apply(lambda x:math.log(x))
    sf_final['Product_Proportion_log_VolumeProportion']=sf_final['VolumeProportion']*sf_final['log_VolumeProportion']
    sf_loc_diversity=sf_final.groupby([callerIdCol],{'loc_diversity_numerator':gl.aggregate.SUM('Product_Proportion_log_VolumeProportion'),'UniqueCells':gl.aggregate.COUNT_DISTINCT('Loc')})
    sf_loc_diversity['Denominator']=sf_loc_diversity['UniqueCells'].apply(lambda x:math.log(float(x)))
    #print sf_loc_diversity['Denominator'].sketch_summary()
    #sf_user=gl.SFrame.read_csv(UserFile, delimiter='\t')[[callerIdCol]]
    #sf_loc_diversity=sf_loc_diversity.join(sf_user, on=callerIdCol, how='inner')
    sf_loc_diversity['loc_diversity']=-sf_loc_diversity['loc_diversity_numerator']/(sf_loc_diversity['Denominator']+1.0)# Total No of possibel cells
    sf_loc_diversity.export_csv('Test_Loc_Diversity.csv', quote_level=csv.QUOTE_NONE)
    sf=sf_loc_diversity[[callerIdCol,'loc_diversity']].unique()
    sf.export_csv(output_file,quote_level=csv.QUOTE_NONE)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Topological Diversity')
    parser.add_argument('-if','--input_file',help='Input File', required=True)
    parser.add_argument('-of','--output_file',help='Output File', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerIdCol', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverIdCol', required=True)
    parser.add_argument('-ccc','--callerCellCol',help='CallerCellCol', required=True)
    parser.add_argument('-rcc','--receiverCellCol',help='ReceiverCellCol', required=True)

    args=parser.parse_args()
    location_diversity(args.input_file, args.output_file, args.callerIdCol, args.receiverIdCol, args.callerCellCol, args.receiverCellCol)
