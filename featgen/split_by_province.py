import pandas as pd
import argparse
import csv
def merge_files_demographics(male_file, female_file,working_male_file,working_female_file,modal_file,demographics_df, prefix='' ):
    
    male_df=pd.read_csv(male_file).reset_index()
    male_df.columns=['Male_'+each  if 'CallerId' not in each else each for each in male_df.columns]
    female_df=pd.read_csv(female_file).reset_index()
    female_df.columns=['Female_'+each   if 'CallerId' not in each else each for each in female_df.columns]
    working_male_df=pd.read_csv(working_male_file).reset_index()
    working_male_df.columns=['WorkingMale_'+each   if 'CallerId' not in each else each for each in working_male_df.columns]
    working_female_df=pd.read_csv(working_female_file).reset_index()
    working_female_df.columns=['WorkingFemale_'+each   if 'CallerId' not in each else each for each in working_female_df.columns]
    
    merged_df=reduce(lambda left,right:pd.merge(left, right, on='CallerId',how='outer'),
                     [male_df, female_df, working_male_df,working_female_df])
    
    modal_df=pd.read_csv(modal_file)
    modal_df.columns=['CallerId','District']
    merged_df=pd.merge(merged_df,modal_df, on='CallerId')
    merged_df=pd.merge(merged_df,demographics_df, left_on='District',right_on='District')
    
    
    
    dfs_list={}
    # Overall
    
    dfs_list['overall']=merged_df.copy()
    merged_df.to_csv('Provincial/'+prefix+'Overall.csv')
    for prov in ['Punjab','Sindh','Balochistan','KP','AJK','FATA']:
        print '*********', prov
        prov_df=merged_df[merged_df.Province==prov].copy()
        dfs_list[prov]=prov_df
        prov_df.to_csv('Provincial/'+prefix+prov+'.csv')
#         print prov_df.describe()
    #Urban
    urban_df=merged_df[merged_df.UrbanProportion>25].copy()
    dfs_list['Urban']=urban_df
    urban_df.to_csv('Provincial/'+prefix+'Urban.csv')
    #Rural
    rural_df=merged_df[merged_df.UrbanProportion<=25].copy()
    dfs_list['Rural']=rural_df
    rural_df.to_csv('Provincial/'+prefix+'Rural.csv')
    print len(dfs_list)
    return dfs_list


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Split data on the basis of Province and Urban Density')
    parser.add_argument('-df','--demographics_file',required=True)
    parser.add_argument('-udf','--urban_density_file',required=True)
    parser.add_argument('-mf','--males_file',required=True)
    parser.add_argument('-ff','--females_file',required=True)
    parser.add_argument('-wmf','--working_males_file',required=True)
    parser.add_argument('-wff','--working_females_file',required=True)
    parser.add_argument('-of','--output_file_prefix',required=False)
    args=parser.parse_args()
    

    
    df_demographics=pd.read_csv(args.demographics_file)[['District','Province']]
    df_UrbanDensity=pd.read_csv(args.urban_density_file)

    merged_df=pd.merge(df_demographics, df_UrbanDensity, on='District')[['District', 'Province', 'UrbanProportion']]
    print merged_df.head()

    prefix=''
    if args.output_file_prefix is not None:
        prefix=args.output_file_prefix
    dfs_list=merge_files_demographics(male_file=args.males_file,
                                      working_male_file=args.working_males_file,
                                      working_female_file=args.working_females_file,
                                      female_file=args.females_file,
                                      modal_file=args.males_file,
                                       demographics_df=merged_df,prefix=prefix)


