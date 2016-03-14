#python gender_diversity_topk.py -if ../data/bidir_gsm_oneaccount_pro2_CDRmub_8-14.csv -pf ../data/profile_info.txt -cc CallerId  -rc ReceiverId -of bidir_gsm_gender_diversity.csv
#python gender_diversity_topk.py -if ../data/bidir_gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of bidir_gsm_sms_gender_diversity.csv -pf ../data/profile_info.txt
#python gender_diversity_topk.py -if ../data/gsm_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of gsm_gender_diversity.csv -pf ../data/profile_info.txt
python gender_diversity_topk.py -if ../data/gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of gsm_sms_gender_diversity.csv -pf ../data/profile_info.txt

#../data/bidir_gsm_oneaccount_pro2_CDRmub_8-14.csv      ../data/gsm_oneaccount_pro2_CDRmub_8-14.csv
#../data/bidir_gsm_sms_oneaccount_pro2_CDRmub_8-14.csv  ../data/gsm_sms_oneaccount_pro2_CDRmub_8-14.csv
#../data/bidir_oneaccount_pro2_CDRmub_8-14.csv          ../data/oneaccount_pro2_CDRmub_8-14.csv

