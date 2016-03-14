python triads_calculation.py -if ../data/bidir_gsm_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of bidir_gsm_triads.csv
python triads_calculation.py -if ../data/bidir_gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of bidir_gsm_sms_triads.csv
python triads_calculation.py -if ../data/gsm_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of gsm_triads.csv
python triads_calculation.py -if ../data/gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -of gsm_sms_triads.csv


