import argparse
import csv
import graphlab as gl

def split_data(modal_file, demographics_file,urban_file, working_status_file,gender_file, output_file):
	modal_sf=gl.SFrame.read_csv(modal_file)[['CallerId','ModalDistrict']].rename({'ModalDistrict':'District'})
	demographics_sf=gl.SFrame.read_csv(demographics_file)[['District','Province']]
	urban_sf=gl.SFrame.read_csv(urban_file)[['District','UrbanProportion']]
	demographics_sf=demographics_sf.join(urban_sf, on='District')
	working_sf=gl.SFrame.read_csv(working_status_file)
	gender_sf=gl.SFrame.read_csv(gender_file, delimiter='\t')[['msisdn','gend']].rename({'msisdn':'CallerId','gend':'gender'})
	merged_sf=modal_sf.join(working_sf, on='CallerId').join(gender_sf, on='CallerId').join(demographics_sf, on='District')
	print 'Shape at district level is', merged_sf.shape
	males_sf=merged_sf.filter_by(1,'gender').groupby('Province',operations={'TotalMales':gl.aggregate.COUNT()})
	females_sf=merged_sf.filter_by(0,'gender').groupby('Province',operations={'TotalFemales':gl.aggregate.COUNT()})
	working_males_sf=merged_sf.filter_by(1,'gender').filter_by(1,'WorkingStatus').groupby('Province',operations={'TotalWorkingMales':gl.aggregate.COUNT()})
	working_females_sf=merged_sf.filter_by(0,'gender').filter_by(1,'WorkingStatus').groupby('Province',operations={'TotalWorkingFemales':gl.aggregate.COUNT()})
	
	final_sf=males_sf.join(females_sf,on='Province',how='outer').join(working_males_sf, on='Province',how='outer').join(working_females_sf, on='Province',how='outer')
	final_sf.export_csv(output_file,quote_level=csv.QUOTE_NONE)


if __name__=='__main__':
	parser=argparse.ArgumentParser(description='Count males and females in each of the district')
	
	parser.add_argument('-lf','--loc_file',help='Modal Location File',required=True)
	parser.add_argument('-gf','--gender_file',help='Gender Info File',required=True)
	parser.add_argument('-df','--demographics_file',help='Demographics File', required=True)
	parser.add_argument('-uf','--urban_file',help='UrbanProportion File', required=True)
	parser.add_argument('-wf','--working_file',help='Working Status File', required=True)
	parser.add_argument('-of','--output_file',help='Output File', required=True)
	
	args=parser.parse_args()
	split_data(args.loc_file, args.demographics_file,args.urban_file, args.working_file,args.gender_file, args.output_file)
