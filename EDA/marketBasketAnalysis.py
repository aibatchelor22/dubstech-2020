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

def getTopXCategories(x):
    '''
    This function gets us the most sold categories from our grocery store dataset
    '''
    vals= rawGSD.groupby(['CATEGORY']).sum().sort_values(['PROFIT'],ascending=False)

    topxCategories=vals.reset_index().CATEGORY.values[0:x]#['Other Vegies','Apples','Potatoes','Citrus','Tomatoes']
    return topxCategories

def plotPivot(data,topx,basketCap=15,save=True):
    unqCats = pd.unique(data.CATEGORY)
    replaceDict = {}
    for c in unqCats:
        if(c not in topx):
            replaceDict[c]='other'
    data.CATEGORY = data.CATEGORY.replace(replaceDict)
    pivottable = pd.pivot_table(data,index=['TICKET'],columns=['CATEGORY'],values='UNITS',aggfunc=len)
    pivottable = pivottable.fillna(0)
    basketSizes=np.sum(pivottable.fillna(0).values,axis=1)
    counter =0
    percentageBasket=pivottable.values
    cs = np.append(topx,'other')
    while(counter < basketSizes.shape[0]):
        percentageBasket[counter,:] = percentageBasket[counter,:]/basketSizes[counter]
        counter+=1
    toagg = pd.DataFrame(np.append(pivottable.values, np.reshape(basketSizes,(-1,1)),axis=1),columns = np.append(cs,'numItems'))
    toagg = toagg.loc[toagg.numItems< basketCap]
    result = toagg.groupby(['numItems']).mean()
    result.plot(kind='bar',stacked=True)
    plt.title("breakdown of categories in a basket per basket size")
    plt.tight_layout()
    if(save):
        plt.savefig('percentageBaskettop10',dpi=80,quality=90)
    else:
        plt.show()

def commonBasketSize(data,topX,addCatInfo = False):
    basketSize= data.groupby('TICKET').count().values[:,0]
    x = len(topX)
    if(addCatInfo is False):
        plt.hist(basketSize)
        plt.xlabel('Basket Size')
        plt.ylabel('Frequency')
        plt.show()
    else:
        categoryDict = {}
        custHist = np.zeros((len(basketSize),x+1))
        counter=0
        for c in topX:
            categoryDict[c] = counter
            counter+=1
        categoryDict['other']=counter
        counter=0
        unqTickets = pd.unique(data.TICKET)
        for t in unqTickets:
            aBasket = data.loc[data.TICKET==t]
            custArr = np.zeros(x+1)
            for c in aBasket.CATEGORY:
                if(c not in categoryDict.keys()):
                    custArr[-1]+=1
                else:
                    custArr[categoryDict[c]]+=1
            custHist[counter]=custArr
            counter+=1
        pdb.set_trace()




if(len(sys.argv)<2):
    print("ERROR: Need path name to data source")
else:
    dataPath = sys.argv[1]
    with open(dataPath+'\\grocery_store_data_cleaned.csv','r') as f:
        rawGSD = pd.read_csv(f,index_col=0) # raw grocery store data
    topX = getTopXCategories(10)
    #commonBasketSize(rawGSD,top5,True)
    plotPivot(rawGSD,topX)
