
#python merge_features.py -df bidir_gsm_degree.csv -vf bidir_gsm_volume.csv -adf bidir_gsm_age_diversity.csv -gdf bidir_gsm_gender_diversity.csv -ldf bidir_gsm_location_diversity.csv -tdf bidir_gsm_topological_diversity.csv -of bidir_gsm_features.csv -mf ../data/ModalDistrict.csv -pf ../data/profile_info.txt

#python merge_features.py -df bidir_gsm_sms_degree.csv -vf bidir_gsm_sms_volume.csv -adf bidir_gsm_sms_age_diversity.csv -gdf bidir_gsm_sms_gender_diversity.csv -ldf bidir_gsm_sms_location_diversity.csv -tdf bidir_gsm_sms_topological_diversity.csv -of bidir_gsm_sms_features.csv -mf ../data/ModalDistrict.csv -pf ../data/profile_info.txt

#python merge_features.py -df gsm_degree.csv -vf gsm_volume.csv -adf gsm_age_diversity.csv -gdf gsm_gender_diversity.csv -ldf gsm_location_diversity.csv -tdf gsm_topological_diversity.csv -of gsm_features.csv -mf ../data/ModalDistrict.csv -pf ../data/profile_info.txt

python merge_features.py -df gsm_sms_degree.csv -vf gsm_sms_volume.csv -adf gsm_sms_age_diversity.csv -gdf gsm_sms_gender_diversity.csv -ldf gsm_sms_location_diversity.csv -tdf gsm_sms_topological_diversity.csv -of gsm_sms_features.csv -mf ../data/ModalDistrict.csv -pf ../data/profile_info.txt -adf2 Top2_gsm_sms_age_diversity.csv -adf4 Top4_gsm_sms_age_diversity.csv -gdf2 Top2_gsm_sms_gender_diversity.csv -gdf4 Top4_gsm_sms_gender_diversity.csv -edf gsm_sms_triads.csv -cdf gsm_sms_constraints.csv -wf gsm_sms_gender_work_status.csv -bcdf gsm_sms_bc.csv
