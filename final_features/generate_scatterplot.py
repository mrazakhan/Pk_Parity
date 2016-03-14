import os
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
#import seaborn as sns
import statsmodels.api as sm
import matplotlib
matplotlib.use('QT4Agg') 
from scipy import stats
from matplotlib import rcParams
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import math
import itertools



#%matplotlib inline
DEBUG=False

#os.chdir('F://PkGenderProjectv3//')
font = {'family' : 'normal',
        #'weight' : 'bold',
        'size'   : 12}

matplotlib.rc('font', **font)

rcParams.update({'figure.autolayout': True})

#sns.set_style('whitegrid')

def scatterplot_matrix(data, names=[], **kwargs):
    """
    Plots a scatterplot matrix of subplots.  Each row of "data" is plotted
    against other rows, resulting in a nrows by nrows grid of subplots with the
    diagonal subplots labeled with "names".  Additional keyword arguments are
    passed on to matplotlib's "plot" command. Returns the matplotlib figure
    object containg the subplot grid.
    """
    numvars, numdata = data.shape
    fig, axes = plt.subplots(nrows=numvars, ncols=numvars, figsize=(160,130))
    fig.subplots_adjust(hspace=0.0, wspace=0.0)
    print len(axes)
    count=0
    for ax in axes.flat:
        print count,
        count+=1
        # Hide all ticks and labels
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        # Set up ticks only on one side for the "edge" subplots...
        if ax.is_first_col():
            ax.yaxis.set_ticks_position('left')
        if ax.is_last_col():
            ax.yaxis.set_ticks_position('right')
        if ax.is_first_row():
            ax.xaxis.set_ticks_position('top')
        if ax.is_last_row():
            ax.xaxis.set_ticks_position('bottom')

    # Plot the data.
    for i, j in zip(*np.triu_indices_from(axes, k=1)):
        for x, y in [(i,j), (j,i)]:
            print x,y
            # FIX #1: this needed to be changed from ...(data[x], data[y],...)
            axes[x,y].plot(data[y], data[x], **kwargs)

    # Label the diagonal subplots...
    if not names:
        names = ['x'+str(i) for i in range(numvars)]

    for i, label in enumerate(names):
        axes[i,i].annotate(label, (0.5, 0.5), xycoords='axes fraction',
                ha='center', va='center')

    # Turn on the proper x or y axes ticks.
    for i, j in zip(range(numvars), itertools.cycle((-1, 0))):
        axes[j,i].xaxis.set_visible(True)
        axes[i,j].yaxis.set_visible(True)

    # FIX #2: if numvars is odd, the bottom right corner plot doesn't have the
    # correct axes limits, so we pull them from other axes
    if numvars%2:
        xlimits = axes[0,-1].get_xlim()
        ylimits = axes[-1,0].get_ylim()
        axes[-1,-1].set_xlim(xlimits)
        axes[-1,-1].set_ylim(ylimits)

	fig.savefig('scatter.png')

    return fig

if __name__=='__main__':

		df=pd.read_csv('district_demographics_gsm_features.csv')
		df['weights']=df['Census_Overall']*100.0/df['Census_Overall'].sum()
		total_population=df['Census_Overall'].sum()

		exclude_list=['District','Province','Rank2015','modified_district','EducationScore','EnrolmentScore','LearningScore',
					  'RetentionScore', 'weights']
		df2=df[[each for each in df.columns if each not in exclude_list]]
		print 'Generating Scatterplot'
		fig=scatterplot_matrix(df2.T)
