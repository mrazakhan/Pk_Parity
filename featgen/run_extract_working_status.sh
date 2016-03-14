#python extract_working_status.py -if ../data/head.txt -pf ../data/head_profile.txt -dc X1 -cc CallerId  -rc ReceiverId -ccc CallerCell -rcc ReceiverCell -of bidir_gsm_gender_work_status.csv
#python extract_working_status.py -if ../data/bidir_gsm_oneaccount_pro2_CDRmub_8-14.csv -pf ../data/profile_info.txt -dc X1 -cc CallerId  -rc ReceiverId -ccc CallerCell -rcc ReceiverCell -of bidir_gsm_gender_work_status.csv
#python extract_working_status.py -if ../data/bidir_gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -dc X1 -ccc CallerCell -rcc ReceiverCell  -of bidir_gsm_sms_gender_work_status.csv -pf ../data/profile_info.txt
#python extract_working_status.py -if ../data/gsm_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -dc X1 -ccc CallerCell -rcc ReceiverCell -of gsm_gender_work_status.csv -pf ../data/profile_info.txt
python extract_working_status.py -if ../data/gsm_sms_oneaccount_pro2_CDRmub_8-14.csv -cc CallerId  -rc ReceiverId -dc X1 -ccc CallerCell -rcc ReceiverCell -of gsm_sms_gender_work_status.csv -pf ../data/profile_info.txt


