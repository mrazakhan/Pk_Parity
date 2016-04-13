import graphlab as gl
import graphlab.aggregate as agg
import math
import argparse
import csv
import sys
# Read SF, Make A Copy, Transpose A and B

def merge_features(input_file,filter_file, output_file):
    sf_input=gl.SFrame.read_csv(input_file, column_type_hints={'rog':float,'AvgGeoReach':float,'AvgGeoReach_FAlter':float})
    sf_filter=gl.SFrame.read_csv(filter_file)['CallerId']
    print 'Input sframe shape before filtering users', sf_input.shape
    sf_input=sf_input.filter_by(sf_filter, 'CallerId',exclude=True)
    print 'Input sframe shape after filtering users', sf_input.shape
    print sf_input.column_names()
    
    rename_dict={ 'Degree':'NetworkSize', 'Degree_FAlter':'FemaleAlter_NetworkSize',\
    'embeddedness':'Embeddedness','embeddedness_FAlter':'FemaleAlter_Embeddedness',\
    'normalized_triangle_count':'TriadicClosure', 'normalized_triangle_count_FAlter':'FemaleAlter_TriadicClosure',\
    'Bw_Centrality':'BetweennessCentrality', 'Bw_Centrality_FAlter':'FemaleAlter_BetweennessCentrality',\
    'age_homophily_calls':'AgeHomophilyCalls','age_homophily_calls_FAlter':'FemaleAlter_AgeHomophilyCalls',\
    'age_homophily_net':'AgeHomophilyNet','age_homophily_net_FAlter':'FemaleAlter_AgeHomophilyNet',\
    'Support':'Support','Support_FAlter':'FemaleAlter_Support',\
    'loc_diversity':'LocationDiversity','Loc_Diversity_FAlter':'FemaleAlter_LocationDiversity',\
    'topological_diversity':'NetworkDiversity','topological_diversity_FAlter':'FemaleAlter_NetworkDiversity',\
    'Constraints':'Constraints','Constraints_FAlter':'FemaleAlter_Constraints',\
    'age_diversity':'AgeDiversity','age_diversity_FAlter':'FemaleAlter_AgeDiversity',\
    'gender_diversity':'GenderDiversity','gender_diversity_FAlter':'FemaleAlter_GenderDiversity',\
    'Count':'Volume','Count_FAlter':'FemaleAlter_Volume',\
    'AvgGeoReach':'AvgGeoReach',\
    'AvgGeoReach_FAlter':'FemaleAlter_AvgGeoReach', \
    'rog':'RadiusOfGyration',\
    'gender_homophily_calls':'GenderHomophilyCalls','gender_homophily_calls_FAlter':'FemaleAlter_GenderHomophilyCalls',\
    'gender_homophily_net':'GenderHomophilyNet','gender_homophily_net_FAlter':'FemaleAlter_GenderHomophilyNet'} 
    sf_input.rename(rename_dict)

 
    sf_males=sf_input.filter_by(1,'gender')
    sf_females=sf_input.filter_by(0,'gender')
    sf_males.remove_column('gender')
    sf_females.remove_column('gender')
    sf_overall=sf_males.append(sf_females)
    sframes_dict={'Male':sf_males, 'Female':sf_females,'Overall':sf_overall}
    out_sfs=[]
    for key in sframes_dict:
        #CallerId,gender,ModalDistrict,Degree,Count,gender_diversity,age_diversity,loc_diversity,topological_diversity
    	ops={'Working_Count_'+key:agg.SUM('WorkingStatus')}
        ops['UsersCount_'+key]=agg.COUNT()
        for col in rename_dict.values():
            print 'PROGRESS: Generating Avg, Mdn and std for {}'.format(col)
            sframes_dict[key][col]=sframes_dict[key][col].apply(lambda x:float(x))
            ops['Avg_'+col+'_'+key]=agg.MEAN(col)
            ops['Mdn_'+col+'_'+key]=agg.QUANTILE(col,0.5)
            ops['Std_'+col+'_'+key]=agg.STD(col)

        
        sf_merged=sframes_dict[key].groupby(['ModalDistrict'], operations=ops)
        for col in sf_merged.column_names():
            if 'Mdn' in col:
                sf_merged[col]=sf_merged[col].apply(lambda x:x[0])
        sf_merged.rename({'ModalDistrict':'District'})
        print '*********************Progress : key', key, sf_merged.column_names()
        out_sfs.append(sf_merged)

    sf_final=out_sfs[0].join(out_sfs[1], how='outer',on='District').join(out_sfs[2], how='outer',on='District')
    sf_final.export_csv(output_file, quote_level=csv.QUOTE_NONE)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Merge Features at District Level')
    parser.add_argument('-if','--input_file',help='Input File', required=True)
    #parser.add_argument('-if','--input_file',help='Input File', required=True)
    parser.add_argument('-of','--output_file',help='Output File', required=True)
    parser.add_argument('-ff','--filter_file',help='Filter File', required=True)

    args=parser.parse_args()
    merge_features(args.input_file, args.filter_file,args.output_file)
