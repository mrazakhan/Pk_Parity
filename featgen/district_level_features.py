import graphlab as gl
import graphlab.aggregate as agg
import math
import argparse
import csv

# Read SF, Make A Copy, Transpose A and B

def merge_features(input_file,filter_file, output_file):
    sf_input=gl.SFrame.read_csv(input_file)
    sf_filter=gl.SFrame.read_csv(filter_file)['CallerId']
    print 'Input sframe shape before filtering users', sf_input.shape
    sf_input=sf_input.filter_by(sf_filter, 'CallerId',exclude=True)
    print 'Input sframe shape after filtering users', sf_input.shape
    #CallerId,gender,ModalDistrict,Degree,Bw_Centrality,Embeddedness,Top4_age_diversity,Top2_age_diversity,Count,gender_homophily_calls,gender_homophily_net,topological_diversity,WorkingStatus,gender_diversity,age_diversity,age_homophily_calls,age_homophily_net,loc_diversity,Top2_gender_diversity,Top4_gender_diversity,Constraints
	#CallerId,gender,ModalDistrict,Degree,Embeddedness,Top4_age_diversity,Top2_age_diversity,Count,topological_diversity,WorkingStatus,gender_diversity,age_diversity,loc_diversity,Top2_gender_diversity,Top4_gender_diversity,Constraints
    sf_input.rename({'Count':'Volume','gender_diversity':'Gender_Div','Top2_gender_diversity':'Top2_Gender_Div',\
    'Top4_gender_diversity':'Top4_Gender_Div','age_diversity':'Age_Div','loc_diversity':'Loc_Div',\
    'Top4_age_diversity':'Top4_Age_Div','age_homophily_calls':'Age_Homophily_Calls',\
    'gender_homophily_calls':'Gender_Homophily_Calls','age_homophily_net':'Age_Homophily_Net',\
    'gender_homophily_net':'Gender_Homophily_Net','Top2_age_diversity':'Top2_Age_Div','topological_diversity':'Net_Div'})
    sf_males=sf_input.filter_by(1,'gender')
    sf_females=sf_input.filter_by(0,'gender')
    sf_males.remove_column('gender')
    sf_females.remove_column('gender')
    sf_overall=sf_males.append(sf_females)
    sframes_dict={'Male':sf_males, 'Female':sf_females,'Overall':sf_overall}
    out_sfs=[]
    ops={'Working_Count':agg.SUM('WorkingStatus')}
    for key in sframes_dict:
        #CallerId,gender,ModalDistrict,Degree,Count,gender_diversity,age_diversity,loc_diversity,topological_diversity
        ops['UsersCount_'+key]=agg.COUNT()
        for col in ['Degree','Volume','Gender_Div','Age_Div','Loc_Div','Net_Div','Embeddedness','Constraints','Top4_Gender_Div','Top2_Gender_Div','Top4_Age_Div','Top2_Age_Div','Gender_Homophily_Calls','Gender_Homophily_Net','Age_Homophily_Calls','Age_Homophily_Net']:
            ops['Avg_'+col+'_'+key]=agg.MEAN(col)
            ops['Mdn_'+col+'_'+key]=agg.QUANTILE(col,0.5)
            ops['Std_'+col+'_'+key]=agg.STD(col)

        
        sf_merged=sframes_dict[key].groupby(['ModalDistrict'], operations=ops)
        for col in sf_merged.column_names():
            if 'Mdn' in col:
                sf_merged[col]=sf_merged[col].apply(lambda x:x[0])
        sf_merged.rename({'ModalDistrict':'District'})
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
