import graphlab as gl
import argparse
import csv

'''
2014-06-06 16:18:35|1.04687517177400E 012|1.04686851202900E 012|SMS|FCN002||.00
2014-06-06 22:27:22|1.04688474474500E 012|1.04660785802400E 012|SMS|MJH009||.00
2014-06-06 10:22:20|1.04691637292400E 012|1.04679597189400E 012|GSM|IAB022||5.00
2014-06-06 14:37:05|1.04691350529900E 012|1.04692342220500E 012|GSM|LSK003||3.00
'''

def extract_gsm(filename):

	sf=gl.SFrame.read_csv(filename, header=False, delimiter='|')
	sf.rename({'X1':'Date','X2':'Caller','X3':'Callee','X4':'Type','X5':'CallerCell','X6':'CalleeCell','X7':'Duration'})
	sf2=sf[['Caller','Callee','CallerCell','CalleeCell','Type']]
	print 'Shape before filtering gsm', sf2.shape
	sf2=sf2.filter_by(values='GSM',column_name='Type')
	
	print 'Shape after filtering gsm', sf2.shape

	sf_caller=sf2[['Caller','CallerCell']]
	sf_callee=sf2[['Callee','CalleeCell']]

	print 'Sf_Caller Shape before filtering None', sf_caller.shape
	print 'SF_Callee Shape before filtering None', sf_callee.shape

	sf_caller=sf_caller.filter_by('','CallerCell',exclude=True)
	sf_callee=sf_callee.filter_by('','CalleeCell',exclude=True)
		
	print 'Sf_Caller Shape after filtering None', sf_caller.shape
	print 'SF_Callee Shape after filtering None', sf_callee.shape

	sf_callee.rename({'Callee':'Caller','CalleeCell':'CallerCell'})

	sf_merged=sf_caller.append(sf_callee)

	sf_merged.export_csv('./gsm_'+filename.split('/')[-1])

if __name__=='__main__':
	
	parser = argparse.ArgumentParser(description='Filter gsm and flatten')
	parser.add_argument('-i', '--input_file', required=True, help="input_file")
	args=parser.parse_args()
	extract_gsm(args.input_file)
