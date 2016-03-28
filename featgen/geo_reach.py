import graphlab as gl
import math
import argparse
import csv
import sys
# Read SF, Make A Copy, Transpose A and B
def distance(self,l1_lat,l1_lng,l2_lat,l2_lng):
    R = 6371; # Radius of the earth in km
    d=0.0
    try:	
        l1_lat, l1_lng, l2_lat, l2_lng=float(l1_lat), float(l1_lng), float(l2_lat), float(l2_lng)
    except:
        l1_lat, l1_lng, l2_lat, l2_lng=0.0,0.0,0.0,0.0
    dLat = (l1_lat-l2_lat)*math.pi/180  
    dLon = (l1_lng-l2_lng)*math.pi/180 
    a = math.sin(dLat/2) * math.sin(dLat/2) +math.cos((l1_lat)*math.pi/180) * math.cos((l2_lat)*math.pi/180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c # Distance in km
    return d

def geo_reach(input_file,loc_file, output_file, callerIdCol, receiverIdCol, callerCellCol, receiverCellCol):
    #Index,TowerId,Lat,Lng,District
    loc_sf=gl.SFrame.read_csv(loc_file)
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
    sf=sf[[callerIdCol, callerCellCol, receiverCellCol]].dropna()
    sf.rename({callerCellCol:'LocA',receiverCellCol:'LocB'})
    print 'Shape before filtering missing towers', sf.shape
    sf=sf.filter_by('', 'LocA', exclude=True).filter_by('','LocB',exclude=True)
    print 'Shape after filtering missing towers', sf.shape
    
    # Joining on the Caller Locations
    sf=sf.join(loc_sf, on='LocA', how='inner')
    sf.rename({'Lat':'LatA','Lng':'LngA'})
    # Joining on the Caller Location
    sf=sf.join(loc_sf, on='LocB', how='inner')
    sf.rename({'Lat':'LatB','Lng':'LngB'})
   
    sf['dist']=sf.apply(lambda x:distance(x['LatA'],x['LngA'],x['LatB'],x['LngB']))
    sf_final=sf.groupby(CallerIdCol, {'AvgGeoReach':gl.aggregate.AVG('dist')})
     
    sf_final.export_csv(output_file,quote_level=csv.QUOTE_NONE)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Topological Diversity')
    parser.add_argument('-if','--input_file',help='Input CDR File', required=True)
    parser.add_argument('-lf','--loc_file',help='Towers Loc File', required=True)
    parser.add_argument('-of','--output_file',help='Output File', required=True)
    parser.add_argument('-cc','--callerIdCol',help='CallerIdCol', required=True)
    parser.add_argument('-rc','--receiverIdCol',help='ReceiverIdCol', required=True)
    parser.add_argument('-ccc','--callerCellCol',help='CallerCellCol', required=True)
    parser.add_argument('-rcc','--receiverCellCol',help='ReceiverCellCol', required=True)

    args=parser.parse_args()
    geo_reach(args.input_file, args.loc_file,args.output_file, args.callerIdCol, args.receiverIdCol, args.callerCellCol, args.receiverCellCol)
