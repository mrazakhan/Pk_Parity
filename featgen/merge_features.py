import graphlab as gl
import math
import argparse
import csv

# Read SF, Make A Copy, Transpose A and B

def merge_features(degree_file,volume_file, age_diversity_file,age_diversity_file_top2, age_diversity_file_top4, gender_diversity_file,gender_diversity_file_top2, gender_diversity_file_top4,  location_diversity_file, topological_diversity_file,embeddedness_file, constraints_file,bw_centrality_file, gender_homophily_file, age_homophily_file, working_status_file,  modal_districts_file,profile_file, output_file):
    sf_degree=gl.SFrame.read_csv(degree_file)[['CallerId','Degree']]
    sf_gender_homophily=gl.SFrame.read_csv(gender_homophily_file)[['CallerId','homophily_calls','homophily_net']].rename({'homophily_calls':'gender_homophily_calls','homophily_net':'gender_homophily_net'})	
    sf_age_homophily=gl.SFrame.read_csv(age_homophily_file)[['CallerId','homophily_calls','homophily_net']].rename({'homophily_calls':'age_homophily_calls','homophily_net':'age_homophily_net'})	
    sf_bw_centrality=gl.SFrame.read_csv(bw_centrality_file)[['CallerId','Bw_Centrality']]
    sf_volume=gl.SFrame.read_csv(volume_file)[['CallerId','Count']]
    sf_working=gl.SFrame.read_csv(working_status_file)[['CallerId','WorkingStatus']]
    sf_age=gl.SFrame.read_csv(age_diversity_file)[['CallerId','age_diversity']]
    sf_age2=gl.SFrame.read_csv(age_diversity_file_top2)[['CallerId','age_diversity']].rename({'age_diversity':'Top2_age_diversity'})
    sf_age4=gl.SFrame.read_csv(age_diversity_file_top4)[['CallerId','age_diversity']].rename({'age_diversity':'Top4_age_diversity'})
    sf_gender=gl.SFrame.read_csv(gender_diversity_file)[['CallerId','gender_diversity']]
    sf_gender2=gl.SFrame.read_csv(gender_diversity_file_top2)[['CallerId','gender_diversity']].rename({'gender_diversity':'Top2_gender_diversity'})
    sf_gender4=gl.SFrame.read_csv(gender_diversity_file_top4)[['CallerId','gender_diversity']].rename({'gender_diversity':'Top4_gender_diversity'})

    sf_location=gl.SFrame.read_csv(location_diversity_file)[['CallerId','loc_diversity']]
    sf_topology=gl.SFrame.read_csv(topological_diversity_file)[['CallerId','topological_diversity']]
    sf_embeddedness=gl.SFrame.read_csv(embeddedness_file)[['CallerId','Embeddedness']]
    sf_constraints=gl.SFrame.read_csv(constraints_file)[['CallerId','Constraints']]
    sf_modal=gl.SFrame.read_csv(modal_districts_file).rename({'MostFrequent':'ModalDistrict'})
    sf_profile=gl.SFrame.read_csv(profile_file, delimiter='\t')[['msisdn','gend']].rename({'msisdn':'CallerId','gend':'gender'})
    sf_merged=sf_degree
    print ' Shape of the merged frame after merging {} is {}'.format( 'degree', sf_degree.shape)
    sframes_dict={'volume':sf_volume,'working':sf_working, 'age':sf_age,'age2':sf_age2, 'age4':sf_age4,  'gender':sf_gender,'gender2':sf_gender2, 'gender4':sf_gender4, 'location':sf_location, 'topology':sf_topology, 'embeddedness':sf_embeddedness, 'constraints':sf_constraints,'bw_centrality':sf_bw_centrality,'gender_homophily':sf_gender_homophily,'age_homophily':sf_age_homophily}

    for key in sframes_dict.keys():
        sf_merged=sf_merged.join(sframes_dict[key], on='CallerId', how='left')
        print ' Shape of the merged frame after merging {} is {}'.format( key, sf_merged.shape)

    

    sf_merged=sf_modal.join(sf_merged, on='CallerId',how='inner')
    print ' Shape of the merged frame after merging {} is {}'.format( 'modal districts data', sf_merged.shape)
    
    sf_merged=sf_profile.join(sf_merged, on='CallerId',how='inner')
    print ' Shape of the merged frame after merging {} is {}'.format( 'profile data', sf_merged.shape)


    sf_merged.export_csv(output_file, quote_level=csv.QUOTE_NONE)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Merge Features')
    parser.add_argument('-df','--degree_file',help='Degree File', required=True)
    parser.add_argument('-vf','--volume_file',help='Volume File', required=True)
    parser.add_argument('-wf','--working_status_file',help='Working Status File', required=True)
    parser.add_argument('-ghdf','--gender_homophily_file',help='Gender Homophily File', required=True)
    parser.add_argument('-ahdf','--age_homophily_file',help='Age Homophily File', required=True)
    parser.add_argument('-bcdf','--bw_centrality_file',help='BW Centrality File', required=True)
    parser.add_argument('-edf','--embeddedness_file',help='Embeddedness File', required=True)
    parser.add_argument('-cdf','--constraints_file',help='Constraints File', required=True)
    parser.add_argument('-adf','--age_diversity_file',help='Age Diversity File', required=True)
    parser.add_argument('-adf2','--age_diversity_file_top2',help='Age Diversity File Top 2 Friends', required=True)
    parser.add_argument('-adf4','--age_diversity_file_top4',help='Age Diversity File Top 4 Friends', required=True)
    parser.add_argument('-gdf','--gender_diversity_file',help='Gender Diversity File', required=True)
    parser.add_argument('-gdf2','--gender_diversity_file_top2',help='Gender Diversity File top 2 Friends', required=True)
    parser.add_argument('-gdf4','--gender_diversity_file_top4',help='Gender Diversity File top 4 friends', required=True)
    parser.add_argument('-tdf','--topological_diversity_file',help='Topological Diversity File', required=True)
    parser.add_argument('-ldf','--location_diversity_file',help='Location Diversity File', required=True)
    parser.add_argument('-mf','--modal_districts_file',help='Modal Districts File', required=True)
    parser.add_argument('-pf','--profile_file',help='Profile File', required=True)
    parser.add_argument('-of','--output_file',help='Output File', required=True)

    args=parser.parse_args()
    merge_features(args.degree_file,args.volume_file, args.age_diversity_file,args.age_diversity_file_top2, args.age_diversity_file_top4, args.gender_diversity_file,args.gender_diversity_file_top2, args.gender_diversity_file_top4, args.location_diversity_file, args.topological_diversity_file,args.embeddedness_file, args.constraints_file,args.bw_centrality_file,args.gender_homophily_file, args.age_homophily_file,args.working_status_file,args.modal_districts_file,args.profile_file, args.output_file)
