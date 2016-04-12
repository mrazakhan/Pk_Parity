import graphlab as gl
import math
import argparse
import csv

# Vars with falter suffix are the ones for the females alter only
def merge_features(degree_file,degree_file_falter, volume_file,volume_file_falter, age_diversity_file,age_diversity_file_falter,\
		age_diversity_file_top2, age_diversity_file_top4,gender_diversity_file,gender_diversity_file_falter,\
		gender_diversity_file_top2, gender_diversity_file_top4,  location_diversity_file,location_diversity_file_falter, \
		net_diversity_file,net_diversity_file_falter,triads_file,triads_file_falter, \
		constraints_file,constraints_file_falter, bw_centrality_file, bw_centrality_file_falter,\
		gender_homophily_file,gender_homophily_file_falter, age_homophily_file,age_homophily_file_falter,\
		georeach_file,georeach_file_falter, support_file,support_file_falter, \
		rog_file,  working_status_file,  modal_districts_file,profile_file, output_file):
    
    #Degree
    sf_degree=gl.SFrame.read_csv(degree_file)[['CallerId','Degree']]
    #Degree FAlter
    sf_degree_falter=gl.SFrame.read_csv(degree_file)[['CallerId','Degree']].rename({'Degree':'Degree_FAlter'})
 
    #Gender Homophily
    sf_gender_homophily=gl.SFrame.read_csv(gender_homophily_file)[['CallerId','homophily_calls','homophily_net']].rename({'homophily_calls':'gender_homophily_calls','homophily_net':'gender_homophily_net'})	
    sf_gender_homophily_falter=gl.SFrame.read_csv(gender_homophily_file_falter)[['CallerId','homophily_calls','homophily_net']].rename({'homophily_calls':'gender_homophily_calls_FAlter','homophily_net':'gender_homophily_net_FAlter'})	
    
    # Age Homophily
    sf_age_homophily=gl.SFrame.read_csv(age_homophily_file)[['CallerId','homophily_calls','homophily_net']].rename({'homophily_calls':'age_homophily_calls','homophily_net':'age_homophily_net'})	
    sf_age_homophily_falter=gl.SFrame.read_csv(age_homophily_file_falter)[['CallerId','homophily_calls','homophily_net']].rename({'homophily_calls':'age_homophily_calls_FAlter','homophily_net':'age_homophily_net_FAlter'})	

    # BW Centrality
    sf_bw_centrality=gl.SFrame.read_csv(bw_centrality_file, header=False)
    sf_bw_centrality.rename({'X1':'CallerId','X2':'Bw_Centrality'})
    sf_bw_centrality_falter=gl.SFrame.read_csv(bw_centrality_file_falter, header=False)
    sf_bw_centrality_falter.rename({'X1':'CallerId','X2':'Bw_Centrality_FAlter'})
    
    #Support
    sf_support=gl.SFrame.read_csv(support_file)[['CallerId','SupportCount','Degree']]
    sf_support['Support']=sf_support['SupportCount']/sf_support['Degree']
    sf_support=sf_support[['CallerId','Support']]
    
    #Support_FAlter
    sf_support_falter=gl.SFrame.read_csv(support_file_falter)[['CallerId','SupportCount','Degree']]
    sf_support_falter['Support_FAlter']=sf_support_falter['SupportCount']/sf_support_falter['Degree']
    sf_support_falter=sf_support_falter[['CallerId','Support_FAlter']]

    #ROG
    sf_rog=gl.SFrame.read_csv(rog_file)[['CallerId','rog']]
    
    #GeoReach
    sf_georeach=gl.SFrame.read_csv(georeach_file)[['CallerId','AvgGeoReach']]
    sf_georeach_falter=gl.SFrame.read_csv(georeach_file_falter)[['CallerId','AvgGeoReach']].rename({'AvgGeoReach':'AvgGeoReach_FAlter'})
    # Call Volume
    sf_volume=gl.SFrame.read_csv(volume_file)[['CallerId','Count']]
    sf_volume_falter=gl.SFrame.read_csv(volume_file)[['CallerId','Count']].rename({'Count':'Count_FAlter'})
    #Working Status
    sf_working=gl.SFrame.read_csv(working_status_file)[['CallerId','WorkingStatus']]
    # Age Diversity
    sf_age=gl.SFrame.read_csv(age_diversity_file)[['CallerId','age_diversity']]
    sf_age_falter=gl.SFrame.read_csv(age_diversity_file_falter)[['CallerId','age_diversity']].rename({'age_diversity':'age_diversity_FAlter'})
    sf_age2=gl.SFrame.read_csv(age_diversity_file_top2)[['CallerId','age_diversity']].rename({'age_diversity':'Top2_age_diversity'})
    sf_age4=gl.SFrame.read_csv(age_diversity_file_top4)[['CallerId','age_diversity']].rename({'age_diversity':'Top4_age_diversity'})
    
    # Gender Diversity
    sf_gender=gl.SFrame.read_csv(gender_diversity_file)[['CallerId','gender_diversity']]
    sf_gender_falter=gl.SFrame.read_csv(gender_diversity_file_falter)[['CallerId','gender_diversity']].rename({'gender_diversity':'gender_diversity_FAlter'})
    sf_gender2=gl.SFrame.read_csv(gender_diversity_file_top2)[['CallerId','gender_diversity']].rename({'gender_diversity':'Top2_gender_diversity'})
    sf_gender4=gl.SFrame.read_csv(gender_diversity_file_top4)[['CallerId','gender_diversity']].rename({'gender_diversity':'Top4_gender_diversity'})

    # Loc Diversity
    sf_location=gl.SFrame.read_csv(location_diversity_file)[['CallerId','loc_diversity']]
    sf_location_falter=gl.SFrame.read_csv(location_diversity_file_falter)[['CallerId','loc_diversity']].rename({'loc_diversity':'Loc_Diversity_FAlter'})
 
    # Net Diversity
    sf_topology=gl.SFrame.read_csv(net_diversity_file)[['CallerId','topological_diversity']]
    sf_topology_falter=gl.SFrame.read_csv(net_diversity_file_falter)[['CallerId','topological_diversity']].rename({'topological_diversity':'topological_diversity_FAlter'})
    
    # Triads
    sf_triads=gl.SFrame.read_csv(triads_file)[['triangle_count','total_degree','embeddedness','SubscriberId']].rename({'SubscriberId':'CallerId'})
    sf_triads['normalized_triangle_count']=sf_triads['triangle_count']/sf_triads['total_degree']
    sf_triads_falter=gl.SFrame.read_csv(triads_file_falter)[['triangle_count','total_degree','embeddedness','SubscriberId']].rename({'SubscriberId':'CallerId','triangle_count':'triangle_count_FAlter','total_degree':'total_degree_FAlter','embeddedness':'embeddedness_FAlter'})
    sf_triads_falter['normalized_triangle_count_FAlter']=sf_triads_falter['triangle_count_FAlter']/(sf_triads_falter['total_degree_FAlter'])
    # Contraints
    sf_constraints=gl.SFrame.read_csv(constraints_file, header=False).rename({'X1':'CallerId','X2':'Constraints'})
    sf_constraints_falter=gl.SFrame.read_csv(constraints_file_falter, header=False).rename({'X1':'CallerId','X2':'Constraints_FAlter'})

    sf_modal=gl.SFrame.read_csv(modal_districts_file)#.rename({'MostFrequent':'ModalDistrict'})
    sf_profile=gl.SFrame.read_csv(profile_file, delimiter='\t')[['msisdn','gend']].rename({'msisdn':'CallerId','gend':'gender'})
    
    sf_degree['CallerId']=sf_degree['CallerId'].apply(lambda x:str(x))
    sf_merged=sf_degree
    
    print ' Shape of the merged frame after merging {} is {}'.format( 'degree', sf_degree.shape)
    sframes_dict={'degree_falter':sf_degree_falter, 'volume':sf_volume,'volume_falter':sf_volume_falter,\
	'working':sf_working, 'age':sf_age,'age_falter':sf_age_falter,'age2':sf_age2, 'age4':sf_age4, \
	'gender':sf_gender,'gender_falter':sf_gender_falter,'gender2':sf_gender2, 'gender4':sf_gender4,\
	'location':sf_location,'location_falter':sf_location_falter, 'topology':sf_topology,'topology_falter':sf_topology_falter,
	'triads':sf_triads,'triads_falter':sf_triads_falter, \
	'constraints':sf_constraints,'constraints_falter':sf_constraints_falter,\
	'bw_centrality':sf_bw_centrality,'bw_centrality_falter':sf_bw_centrality_falter,\
	'gender_homophily':sf_gender_homophily,'gender_homophily_falter':sf_gender_homophily_falter,\
	'age_homophily':sf_age_homophily,'age_homophily_falter':sf_age_homophily_falter,
	'support':sf_support,'support_falter':sf_support_falter, 'rog':sf_rog,'georeach':sf_georeach,\
	 'georeach_falter':sf_georeach_falter}

    for key in sframes_dict.keys():
        print 'Merge key', key
        sframes_dict[key]['CallerId']=sframes_dict[key]['CallerId'].apply(lambda x:str(x))  
        sf_merged=sf_merged.join(sframes_dict[key], on='CallerId', how='left')
        print ' Shape of the merged frame after merging {} is {}'.format( key, sf_merged.shape)

    
    sf_modal['CallerId']=sf_modal['CallerId'].apply(lambda x:str(x))
    sf_merged=sf_modal.join(sf_merged, on='CallerId',how='inner')
    print ' Shape of the merged frame after merging {} is {}'.format( 'modal districts data', sf_merged.shape)
    
    sf_profile['CallerId']=sf_profile['CallerId'].apply(lambda x:str(x))
    sf_merged=sf_profile.join(sf_merged, on='CallerId',how='inner')
    print ' Shape of the merged frame after merging {} is {}'.format( 'profile data', sf_merged.shape)


    sf_merged.export_csv(output_file, quote_level=csv.QUOTE_NONE)
    sf_merged.filter_by(0, 'Count',exclude=True).filter_by(1, 'Count',exclude=True).export_csv(output_file.split('.')[0]+'_filterCall_g2.csv',quote_level=csv.QUOTE_NONE)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Merge Features')
    parser.add_argument('-df','--degree_file',help='Degree File', required=True)
    parser.add_argument('-dff','--degree_file_falter',help='Degree File Female Alter', required=True)
    parser.add_argument('-vf','--volume_file',help='Volume File', required=True)
    parser.add_argument('-vff','--volume_file_falter',help='Volume File Female Alter', required=True)
    parser.add_argument('-ghdf','--gender_homophily_file',help='Gender Homophily File', required=True)
    parser.add_argument('-ghdff','--gender_homophily_file_falter',help='Gender Homophily Female Alter', required=True)
    parser.add_argument('-ahdf','--age_homophily_file',help='Age Homophily File', required=True)
    parser.add_argument('-ahdff','--age_homophily_file_falter',help='Age Homophily Female Alter', required=True)
    parser.add_argument('-bcdf','--bw_centrality_file',help='BW Centrality File', required=True)
    parser.add_argument('-bcdff','--bw_centrality_file_falter',help='BW Centrality Female Alter', required=True)
    parser.add_argument('-tdf','--triads_file',help='Triads File', required=True)
    parser.add_argument('-tdff','--triads_file_falter',help='Triads Female Alter', required=True)
    parser.add_argument('-cdf','--constraints_file',help='Constraints File', required=True)
    parser.add_argument('-cdff','--constraints_file_falter',help='Constraints Female Alter', required=True)
    parser.add_argument('-adf','--age_diversity_file',help='Age Diversity File', required=True)
    parser.add_argument('-adff','--age_diversity_file_falter',help='Age Diversity Female Alter', required=True)
    parser.add_argument('-adf2','--age_diversity_file_top2',help='Age Diversity File Top 2 Friends', required=True)
    parser.add_argument('-adf4','--age_diversity_file_top4',help='Age Diversity File Top 4 Friends', required=True)
    parser.add_argument('-gdf','--gender_diversity_file',help='Gender Diversity File', required=True)
    parser.add_argument('-gdff','--gender_diversity_file_falter',help='Gender Diversity Female Alter', required=True)
    parser.add_argument('-gdf2','--gender_diversity_file_top2',help='Gender Diversity File top 2 Friends', required=True)
    parser.add_argument('-gdf4','--gender_diversity_file_top4',help='Gender Diversity File top 4 friends', required=True)
    parser.add_argument('-ndf','--net_diversity_file',help='Topological Diversity File', required=True)
    parser.add_argument('-ndff','--net_diversity_file_falter',help='Topological Diversity Female Alter', required=True)
    parser.add_argument('-ldf','--location_diversity_file',help='Location Diversity File', required=True)
    parser.add_argument('-ldff','--location_diversity_file_falter',help='Location Diversity Female Alter', required=True)
    parser.add_argument('-mf','--modal_districts_file',help='Modal Districts File', required=True)
    parser.add_argument('-pf','--profile_file',help='Profile File', required=True)
    parser.add_argument('-of','--output_file',help='Output File', required=True)
    parser.add_argument('-grdf','--georeach_file',help='Geo reach File', required=True)
    parser.add_argument('-grdff','--georeach_file_falter',help='Geo Reach Female Falter', required=True)
    parser.add_argument('-sdf','--support_file',help='support File', required=True)
    parser.add_argument('-sdff','--support_file_falter',help='support File Falter', required=True)
    parser.add_argument('-rdf','--rog_file',help='rog File', required=True)
    parser.add_argument('-wf','--working_status_file',help='Working Status File', required=True)

    args=parser.parse_args()
    merge_features(degree_file=args.degree_file,degree_file_falter=args.degree_file_falter,\
	volume_file=args.volume_file,volume_file_falter=args.volume_file_falter, \
	age_diversity_file=args.age_diversity_file,age_diversity_file_falter=args.age_diversity_file_falter,\
	age_diversity_file_top2=args.age_diversity_file_top2, age_diversity_file_top4=args.age_diversity_file_top4,\
	gender_diversity_file=args.gender_diversity_file,gender_diversity_file_falter=args.gender_diversity_file_falter,\
	gender_diversity_file_top2=args.gender_diversity_file_top2, gender_diversity_file_top4=args.gender_diversity_file_top4,\
	location_diversity_file= args.location_diversity_file,location_diversity_file_falter=args.location_diversity_file_falter,\
	net_diversity_file=args.net_diversity_file,net_diversity_file_falter=args.net_diversity_file_falter,\
	triads_file=args.triads_file,triads_file_falter=args.triads_file_falter,\
	constraints_file=args.constraints_file,constraints_file_falter=args.constraints_file_falter, \
	bw_centrality_file=args.bw_centrality_file,bw_centrality_file_falter=args.bw_centrality_file_falter, \
	gender_homophily_file=args.gender_homophily_file,gender_homophily_file_falter=args.gender_homophily_file_falter,\
	age_homophily_file= args.age_homophily_file,age_homophily_file_falter=args.age_homophily_file_falter,\
	georeach_file=args.georeach_file, georeach_file_falter=args.georeach_file_falter,\
	support_file=args.support_file,support_file_falter=args.support_file_falter,\
	rog_file=args.rog_file,working_status_file=args.working_status_file,modal_districts_file=args.modal_districts_file,\
	profile_file=args.profile_file, output_file=args.output_file)

