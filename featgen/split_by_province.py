import pandas as pd
def merge_files_demographics(male_file, female_file,working_male_file,working_female_file,modal_file,demographics_df ):
    
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
    merged_df.to_csv('Provincial/Overall.csv')
    for prov in ['Punjab','Sindh','Balochistan','KP','AJK','FATA']:
        print '*********', prov
        prov_df=merged_df[merged_df.Province==prov].copy()
        dfs_list[prov]=prov_df
        prov_df.to_csv('Provincial/'+prov+'.csv')
#         print prov_df.describe()
    #Urban
    urban_df=merged_df[merged_df.UrbanProportion>25].copy()
    dfs_list['Urban']=urban_df
    urban_df.to_csv('Provincial/Urban.csv')
    #Rural
    rural_df=merged_df[merged_df.UrbanProportion<=25].copy()
    dfs_list['Rural']=rural_df
    rural_df.to_csv('Provincial/Rural.csv')
    print len(dfs_list)
    return dfs_list



df_demographics=pd.read_csv('../data/Demographics.csv')[['District','Province']]
df_UrbanDensity=pd.read_csv('../data/UrbanProportion.csv')

merged_df=pd.merge(df_demographics, df_UrbanDensity, on='District')[['District', 'Province', 'UrbanProportion']]
print merged_df.head()


dfs_list=merge_files_demographics(male_file='Males_gsm_sms_features.csv',
                                      working_male_file='WorkingMales_gsm_sms_features.csv',
                                      working_female_file='WorkingFemales_gsm_sms_features.csv',
                                      female_file='Females_gsm_sms_features.csv',
                                      modal_file='../data/ModalDistrict.csv',
                                       demographics_df=merged_df)


