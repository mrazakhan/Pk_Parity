#python geo_reach.py -if ../data/bidir_gsm_oneaccount_pro2_CDRmub_8-14.csv -lf ../data/districts.csv -cc CallerId  -rc ReceiverId -ccc CallerCell -rcc ReceiverCell -of bidir_gsm_geo_reach.csv
#python geo_reach.py -if ../data/bidir_gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -lf ../data/districts.csv -cc CallerId  -rc ReceiverId -ccc CallerCell -rcc ReceiverCell -of bidir_gsm_sms_geo_reach.csv
#python geo_reach.py -if ../data/gsm_oneaccount_pro2_CDRmub_8-14.csv -lf ../data/districts.csv -cc CallerId  -rc ReceiverId -ccc CallerCell -rcc ReceiverCell -of gsm_geo_reach.csv
python geo_reach.py -if ../data/gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -lf ../data/districts.csv -cc CallerId  -rc ReceiverId -ccc CallerCell -rcc ReceiverCell -of gsm_sms_geo_reach.csv -pf ../data/AgeInfo.csv


