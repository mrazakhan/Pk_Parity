import graphlab as gl
import math
import argparse
import csv
from collections import Counter

# Read SF, Make A Copy, Transpose A and B

def getHour(x):
	hour=-1
	try:
		hour=int(x.split(' ')[1].split(':')[0])
	except:
		pass
	return hour

def getDayTime(x):
	if x<9 or x>18:
		return 0
	else:
		return 1

def checkDayNight(x):
	ret=0
	if len(x)==2 and x[0]==x[1]:
		return 1
	else:
		return 0

def working_status(input_file,profile_file, output_file,dateTimeCol, callerIdCol, receiverIdCol,callerCellCol,receiverCellCol):
    sf_gender=gl.SFrame.read_csv(profile_file,delimiter='\t')
    print sf_gender.head()
    #return
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
    sf=sf[[dateTimeCol,callerIdCol, callerCellCol]].dropna()
    sf.rename({callerCellCol:'Loc'})
    print 'Shape before removing empty strings from the Loc column', sf.shape
    sf=sf.filter_by('', 'Loc', exclude=True)
    print 'Shape after removing empty strings from the Loc column', sf.shape

    sf_gender.rename({'msisdn':callerIdCol})
    #sf_gender=sf_gender.filter_by(0,'gend')
    sf_merged=sf.join(sf_gender, how='inner', on=callerIdCol)

	
    sf_merged['Hour']=sf_merged[dateTimeCol].apply(lambda x:getHour(x))

    sf_merged['DayTime']=sf_merged['Hour'].apply(lambda x:getDayTime(x))
    print sf_merged.head()
    sf_merged.export_csv('FemaleMergedLocations.csv', quote_level=csv.QUOTE_NONE)

    sf_locs=sf_merged.groupby([callerIdCol,'DayTime'],{'Locations':gl.aggregate.CONCAT('Loc')})
    sf_locs['ModalTower']=sf_locs['Locations'].apply(lambda x:Counter(x).most_common(1)[0][0])
    sf_locs.export_csv('ListLocations.csv', quote_level=csv.QUOTE_NONE)

    sf_working=sf_locs.groupby(callerIdCol,{'DayNightLocs':gl.aggregate.CONCAT('ModalTower')})
    print sf_working.head()
    sf_working['WorkingStatus']=sf_working['DayNightLocs'].apply(lambda x:checkDayNight(x))
	
    sf_working[[callerIdCol,'WorkingStatus']].export_csv(output_file,quote_level=csv.QUOTE_NONE)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='WorkingStatus')
    parser.add_argument('-if','--input_file',help='Input File', required=True)
    parser.add_argument('-pf','--profile_file',help='Profile File', required=True)
    parser.add_argument('-of','--output_file',help='Output File', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerIdCol', required=True)
    parser.add_argument('-ccc','--callerCellCol',help='CallerCellCol', required=True)
    parser.add_argument('-rcc','--receiverCellCol',help='ReceiverIdCol', required=True)
    parser.add_argument('-dc','--dateCol',help='DateCol', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverIdCol', required=True)

    args=parser.parse_args()
    working_status(args.input_file,args.profile_file, args.output_file,args.dateCol, args.callerIdCol, args.receiverIdCol, args.callerCellCol, args.receiverCellCol)
