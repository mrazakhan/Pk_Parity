for each in `ls /data/telenor/CDR/jun14/zips/10_days/2014-06-*`
do 
	echo $each

	python modal_towers.py -i $each
done
