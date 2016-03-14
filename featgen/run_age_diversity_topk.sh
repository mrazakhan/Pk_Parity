#python age_diversity_topk.py -if ../data/bidir_gsm_oneaccount_pro2_CDRmub_8-14.csv -pf ../data/AgeInfo.csv -cc CallerId  -rc ReceiverId -of bidir_gsm_age_diversity.csv
#python age_diversity_topk.py -if ../data/bidir_gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of bidir_gsm_sms_age_diversity.csv -pf ../data/AgeInfo.csv
python age_diversity_topk.py -if ../data/gsm_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of gsm_age_diversity.csv -pf ../data/AgeInfo.csv
python age_diversity_topk.py -if ../data/gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of gsm_sms_age_diversity.csv -pf ../data/AgeInfo.csv

#../data/bidir_gsm_oneaccount_pro2_CDRmub_8-14.csv      ../data/gsm_oneaccount_pro2_CDRmub_8-14.csv
#../data/bidir_gsm_sms_oneaccount_pro2_CDRmub_8-14.csv  ../data/gsm_sms_oneaccount_pro2_CDRmub_8-14.csv
#../data/bidir_oneaccount_pro2_CDRmub_8-14.csv          ../data/oneaccount_pro2_CDRmub_8-14.csv

