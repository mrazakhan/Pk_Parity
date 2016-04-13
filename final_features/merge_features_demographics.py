import graphlab as gl
import argparse
import csv
import sys

def merge_features_demographics(features_file, demographics_file, output_file):
	ff=gl.SFrame.read_csv(features_file)
	#ff['District']=ff['District'].apply(lambda x:CorrectDistrictNames(x))
	'''ff file heade
	Rank2015,modified_district,EducationScore,EnrolmentScore,LearningScore,RetentionScore,GenderParityScore,Voters_Male,Voters_Female,District,Census_Male,Census_Female
	'''
	df=gl.SFrame.read_csv(demographics_file)

	'''df file header
	'''
	df_Districts=df['District']
	ff_Districts=ff['District']

	print 'Districts Missing in CDR',sorted(set(df_Districts)-set(ff_Districts))
	print 'Districts Missing in Demographics'
	for each in sorted(set(ff_Districts)-set(df_Districts)):
		print each.decode('utf-8'),' ',
	merged_df=ff.join(df, on='District')
	
	merged_df['Voters_Overall']=merged_df['Voters_Male']+merged_df['Voters_Female']
	merged_df['Census_Overall']=merged_df['Census_Male']+merged_df['Census_Female']
	print merged_df.column_names()
	#sys.exit(0)
	for col in list(merged_df.select_columns([int,float]).column_names()):
       
		print 'Generating Proportion and Ratio for ', col
		if col in ['UsersCount','Voters','Census']:
			merged_df['Ratio_'+col]=merged_df[col+'_Female']/merged_df[col+'_Male']
			merged_df['Proportion_'+col]=merged_df[col+'_Female']/merged_df[col+'_Overall']
			
		else:
			for transform in ['Mdn','Avg','Std']:
				
				merged_df['Ratio_'+transform+'_'+col]=merged_df[transform+'_'+col+'_Female']/merged_df[transform+'_'+col+'_Male']
				merged_df['Proportion_'+transform+'_'+col]=merged_df[transform+'_'+col+'_Female']/merged_df[transform+'_'+col+'_Overall']
			
	merged_df.export_csv(output_file, quote_level=csv.QUOTE_NONE)
	 
if __name__=='__main__':
	parser=argparse.ArgumentParser(description = 'Merge features file and demographics file')
	parser.add_argument('-cf','--cdr_features_file',help='CDR Features File',required=True)
	parser.add_argument('-df','--demographics_features_file',help='Demographics Features File',required=True)
	parser.add_argument('-of','--output_file',help='Output File',required=True)
	args=parser.parse_args()

	merge_features_demographics(args.cdr_features_file, args.demographics_features_file, args.output_file)

	
