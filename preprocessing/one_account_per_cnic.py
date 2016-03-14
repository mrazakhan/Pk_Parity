import graphlab as gl
import graphlab.aggregate as agg
import csv
import argparse


def filter(inputfilename, outputfilename):
    demographics=gl.SFrame.read_csv(inputfilename,delimiter='\t')
    sf2=demographics[['msisdn','cnic']]

    account_per_cnic = sf2.groupby(key_columns='cnic',operations={'count': agg.COUNT()})

    one_account_per_cnic=account_per_cnic.filter_by(1,'count')[['cnic']]

    final_df=demographics.join(one_account_per_cnic, on='cnic')
    final_df.export_csv(outputfilename,quote_level=csv.QUOTE_NONE)

    
if __name__=='__main__':
    #/data/telenor/CDR/oct15/zips/bvs2.txt
    parser=argparse.ArgumentParser(description='Filter one account per cnic users')
    parser.add_argument('-o','--output', required=True, help='outputfilename')
    parser.add_argument('-i','--input', required=True, help='inputfilename')
    args=parser.parse_args()
    outfile=args.output
    infile=args.input
    filter(infile, outfile)
