#python rog.py -if ../data/bidir_gsm_oneaccount_pro2_CDRmub_8-14.csv -lf ../data/districts.csv -cc CallerId  -rc ReceiverId -ccc CallerCell -rcc ReceiverCell -of bidir_gsm_rog.csv
#python rog.py -if ../data/bidir_gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -lf ../data/districts.csv -cc CallerId  -rc ReceiverId -ccc CallerCell -rcc ReceiverCell -of bidir_gsm_sms_rog.csv
#python rog.py -if ../data/gsm_oneaccount_pro2_CDRmub_8-14.csv -lf ../data/districts.csv -cc CallerId  -rc ReceiverId -ccc CallerCell -rcc ReceiverCell -of gsm_rog.csv
python rog.py -if ../data/gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -lf ../data/districts.csv -cc CallerId  -rc ReceiverId -ccc CallerCell -rcc ReceiverCell -of gsm_sms_rog.csv

#../data/bidir_gsm_oneaccount_pro2_CDRmub_8-14.csv      ../data/gsm_oneaccount_pro2_CDRmub_8-14.csv
#../data/bidir_gsm_sms_oneaccount_pro2_CDRmub_8-14.csv  ../data/gsm_sms_oneaccount_pro2_CDRmub_8-14.csv
#../data/bidir_oneaccount_pro2_CDRmub_8-14.csv          ../data/oneaccount_pro2_CDRmub_8-14.csv

