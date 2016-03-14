import graphlab as gl
import csv
import sys

if __name__=='__main__':

	filename=sys.argv[1]
	sf=gl.SFrame.read_csv(filename)
	print 'shape of the original data frame', sf.shape
	sf_males=sf.filter_by(1, 'gender')
	sf_females=sf.filter_by(0,'gender')
	print 'shape of the males df' , sf_males.shape
	print 'shape of the females df' , sf_females.shape

	sf_males.export_csv('Males_'+filename)
	sf_females.export_csv('Females_'+filename)
