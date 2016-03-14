import graphlab as gl
import math
import argparse
import csv

def agegroups(x):
    if x<25:
	    return 'Young'
    elif x<40:
	    return 'Middle'
    elif x<50:
	    return 'Senior'
    else:
	    return 'Old'
# Read SF, Make A Copy, Transpose A and B

def age_diversity(input_file,profile_file, output_file, callerIdCol, receiverIdCol):
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


    sf_age=gl.SFrame.read_csv(profile_file,delimiter=',')
    sf_age.rename({'msisdn':receiverIdCol})

    sf_merged=sf.join(sf_age, how='inner', on=receiverIdCol)

    sf_merged['age_group']=sf_merged['age'].apply(lambda x:agegroups(x))


    sf_age_group_overall=sf_merged.groupby([callerIdCol,'age_group'],{'AgeGroupTotal':gl.aggregate.COUNT()})

    sf_total=sf_merged.groupby(callerIdCol,{'OverallTotal':gl.aggregate.COUNT(),'UniqueAgeGroups':gl.aggregate.COUNT_DISTINCT('age_group')})

    sf_final=sf_age_group_overall.join(sf_total,on=callerIdCol, how='inner')

    sf_final['VolumeProportion']=sf_final['AgeGroupTotal']/sf_final['OverallTotal']

    sf_final['log_VolumeProportion']=sf_final['VolumeProportion'].apply(lambda x:math.log(x))

    sf_final['Product_Proportion_log_VolumeProportion']=sf_final['VolumeProportion']*sf_final['log_VolumeProportion']

    sf_numerator=sf_final.groupby(callerIdCol,{'age_diversity_numerator':gl.aggregate.SUM('Product_Proportion_log_VolumeProportion')})

    sf_age_diversity=sf_final.join(sf_numerator,on=callerIdCol, how='inner')[[callerIdCol,'age_diversity_numerator','UniqueAgeGroups']]

    sf_age_diversity['age_denominator']=sf_age_diversity['UniqueAgeGroups'].apply(lambda x:math.log(x))

    sf_age_diversity['age_diversity']=-sf_age_diversity['age_diversity_numerator']/(sf_age_diversity['age_denominator']+1.0)

    sf_age_diversity=sf_age_diversity.unique()
    sf_age_diversity.export_csv(output_file, quote_level=csv.QUOTE_NONE)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Topological Diversity')
    parser.add_argument('-if','--input_file',help='Input File', required=True)
    parser.add_argument('-pf','--profile_file',help='Profile File', required=True)
    parser.add_argument('-of','--output_file',help='Output File', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerIdCol', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverIdCol', required=True)

    args=parser.parse_args()
    age_diversity(args.input_file,args.profile_file, args.output_file, args.callerIdCol, args.receiverIdCol)
