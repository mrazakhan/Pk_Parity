#python topological_diversity.py -if ../data/bidir_gsm_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of bidir_gsm_topological_diversity.csv
#python topological_diversity.py -if ../data/bidir_gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of bidir_gsm_sms_topological_diversity.csv
#python topological_diversity.py -if ../data/gsm_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of gsm_topological_diversity.csv
python topological_diversity.py -if ../data/gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of gsm_sms_topological_diversity.csv -pf ../data/profile_info.txt

