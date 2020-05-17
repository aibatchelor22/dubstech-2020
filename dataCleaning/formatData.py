import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import holidays
from datetime import date
import sys
from datetime import date
import pdb


au_holidays = holidays.AU(years=[2016,2017,2018,2019]) # this gets us a dictionary of dates for holidays in Australia
AUHOLIDAYS = list(au_holidays.keys())

def lookatData():
    print(rawGSD.head(10))
    print(rawGSD.describe())
    rawGSD.hist(figsize=(25,20))
    plt.show()

def getTop5Categories():
    '''
    This function gets us the most sold categories from our grocery store dataset
    '''
    vals= rawGSD.groupby(['CATEGORY']).sum().sort_values(['PROFIT'],ascending=False)

    top5Categories=vals.reset_index().CATEGORY.values[0:5]#['Other Vegies','Apples','Potatoes','Citrus','Tomatoes']
    return top5Categories

def getTotalWeekly(data,colInterest=None,save=False,fileName=''):
    '''
    Use the save parameter to save the table to the data directory specified as a csv
    Use the colInterest parameter to indicate a particular column or columns of interest to keep when saving or returning
    Use fileName to specify an additional name to your savefile path or name
    '''
    tochange = data.copy(deep=True)
    tochange.DATE= pd.to_datetime([x[0:x.index(' ')] for x in data.DATE.astype(str)])
    dailyTotals = tochange.groupby('DATE').sum()
    '''
    removing first and last day due to potential not full day operation
    '''
    missingDataPiece = dailyTotals.iloc[dailyTotals.index == min(dailyTotals.index)].UNITS
    dailyTotals = dailyTotals.iloc[dailyTotals.index != min(dailyTotals.index)]
    dailyTotals = dailyTotals.iloc[dailyTotals.index != max(dailyTotals.index)]
    dailyTotals['holidayWeekS'] = dailyTotals.reset_index().DATE.dt.date.isin(AUHOLIDAYS).astype(int).values #column to let us know if there are any holidays this week, for each unit increase represents increasing number of holidays
    if(save):
        if(colInterest is None):
            (dailyTotals.resample('W-MON', label='left').sum()).to_csv(dataPath+'/weekly'+fileName+'.csv')
        else:
            (dailyTotals.resample('W-MON', label='left').sum()[colInterest]).to_csv(dataPath+'/weekly'+colInterest+fileName+'.csv')
    else:
        if(colInterest is None):
            return (dailyTotals.resample('W-MON', label='left').sum())
        else:
            return (dailyTotals.resample('W-MON', label='left').sum()[[colInterest,'holidayWeekS']])
if(len(sys.argv)<2):
    print("ERROR: Need path name to data source")
else:
    dataPath = sys.argv[1]
    with open(dataPath+'\\grocery_store_data_cleaned.csv','r') as f:
        rawGSD = pd.read_csv(f,index_col=0) # raw grocery store data
    #lookatData()
    pdb.set_trace()
    print(getTotalWeekly(rawGSD,'TOTAL_PRICESELL'))
    #Now lets get the same data as above, but for each of the top 5 categories
    top5 = getTop5Categories()
    for c in top5:
        #print(getTotalWeekly(rawGSD.loc[rawGSD.CATEGORY==c],'TOTAL_PRICESELL',True,fileName=c)) #if you want to save the files we used in this report
        print(getTotalWeekly(rawGSD.loc[rawGSD.CATEGORY==c],'TOTAL_PRICESELL',False,fileName=c).head())
