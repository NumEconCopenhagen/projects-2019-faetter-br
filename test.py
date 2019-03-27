#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
# You can load your python module as this:
#import dataproject.example
import requests        # Needed to download the data from Statistics Denmark's API
import io              # Also needed to download the data from Statistics Denmark's API
import pandas as pd    # Pandas - because everybody loves pandas
import matplotlib.pyplot as plt
import numpy as np

# In[2]: Import data from statistics Denmark - population forecast and employment statistics

#GAMbf = pd.read_excel(r'C:\Users\B030526\Documents\Kursus\projects-2019-faetter-br\dataproject\data\BFgammel.xlsx', header = 2) #Imports historical popualtion
#FREMbf = pd.read_excel(r'C:\Users\B030526\Documents\Kursus\projects-2019-faetter-br\dataproject\data\BFfremskrivning.xlsx', header = 2) #Imports Population forecast

#FREMbf.reset_index(inplace=True) #Resets indecies, so "age", "gender" and "origin" can be created as collumn indecies
#FREMbf.rename( columns = {"level_0":"gender", "level_1":"origin", "level_2":"age"}, inplace=True) #Creates "age", "gender" and "origin" variables
#FREMbf["age"] = FREMbf["age"].astype(str).str.split(" ", 1, expand=True) #picks up the integer part(before first space) of the age variable.

#GAMbf.reset_index(inplace=True) #Resets indecies, so "age", "gender" and "origin" can be created as collumn indecies
#GAMbf.rename( columns = {"level_1":"gender", "level_2":"origin", "level_3":"age"}, inplace=True) #Creates "age", "gender" and "origin" variables
#GAMbf["age"] = GAMbf["age"].astype(str).str.split(" ", 1, expand=True) #picks up the integer part(before first space) of the age variable.
#GAMbf["age"] = GAMbf["age"].astype(int)

#Imports employment data directly from DST
RAS200 = requests.get('https://api.statbank.dk/v1/data/RAS200/CSV?valuePresentation=Value&delimiter=Semicolon&BEREGNING=*&TID=*&ALDER=16-17%2C18-19%2C20-24%2C25-29%2C30-34%2C35-39%2C40-44%2C45-49%2C50-54%2C55-59%2C60-64&HERKOMST=10%2C24%2C25%2C34%2C35&K%C3%98N=M%2CK&OMR%C3%85DE=000').content
RAS200 = pd.read_csv(io.StringIO(RAS200.decode('utf-8')),decimal=",",sep=";")
RAS200.loc[:,"INDHOLD"].astype(float) #converts frequencies to floats from strings

GAMbf = requests.get('https://api.statbank.dk/v1/data/FOLK2/CSV?delimiter=Semicolon&ALDER=*&K%C3%98N=*&HERKOMST=*&STATSB=*&Tid=2008%2C2009%2C2010%2C2011%2C2012%2C2013%2C2014%2C2015%2C2016%2C2017').content
GAMbf = pd.read_csv(io.StringIO(GAMbf.decode('utf-8')),decimal=",",sep=";")
GAMbf.loc[:,"INDHOLD"].astype(float) #converts frequencies to floats from strings

FREMbf = requests.get('https://api.statbank.dk/v1/data/FRDK118/CSV?HERKOMST=*&K%C3%98N=*&ALDER=*&Tid=*').content
FREMbf = pd.read_csv(io.StringIO(FREMbf.decode('utf-8')),decimal=",",sep=";")
FREMbf.loc[:,"INDHOLD"].astype(float) #converts frequencies to floats from strings

# In[3]: Creates indexes to match origin and gender in forecast data
i=0
while i<126:
    FREMbf.iat[i, 0] = "M"  #Male gender
    FREMbf.iat[i, 1] = "da" #Danish origin
    i=i+1
i=126
while i<252:
    FREMbf.iat[i, 0] = "M" #Male gender
    FREMbf.iat[i, 1] = "iw" #Western immigrants
    i=i+1
i=252
while i<378:
    FREMbf.iat[i, 0] = "M"#Male gender
    FREMbf.iat[i, 1] = "ix" #Non-western immigrants
    i=i+1
i=378
while i<504:
    FREMbf.iat[i, 0] = "M" #Male gender
    FREMbf.iat[i, 1] = "dw" #Western decendants
    i=i+1
i=504 
while i<630:
    FREMbf.iat[i, 0] = "M"
    FREMbf.iat[i, 1] = "dx" #Non-western decendants
    i=i+1
i=630
while i<756:
    FREMbf.iat[i, 0] = "K"
    FREMbf.iat[i, 1] = "da"
    i=i+1
i=756
while i<882:
    FREMbf.iat[i, 0] = "K"  #Female gender
    FREMbf.iat[i, 1] = "iw" #Western immigrants
    i=i+1
i=882
while i<1008:
    FREMbf.iat[i, 0] = "K" #Female gender
    FREMbf.iat[i, 1] = "ix" #Non-Western immigrants
    i=i+1
i=1008
while i<1134:
    FREMbf.iat[i, 0] = "K"#Female gender
    FREMbf.iat[i, 1] = "dw" #Western decendants
    i=i+1
i=1134
while i<1260:
    FREMbf.iat[i, 0] = "K" #Female gender
    FREMbf.iat[i, 1] = "dx" #Non-Western decendants
    i=i+1


# In[4]: Creates indexes to match origin and gender in historical data
i=0
while i<126:
    GAMbf.iat[i, 1] = "M"  #Male gender
    GAMbf.iat[i, 2] = "da" #Danish origin
    i=i+1
i=126
while i<252:
    GAMbf.iat[i, 1] = "K" #Male gender
    GAMbf.iat[i, 2] = "da" #Western immigrants
    i=i+1
i=252


i=1008
while i<1134:
    GAMbf.iat[i, 1] = "M"#Male gender
    GAMbf.iat[i, 2] = "iw" #western immigrants
    i=i+1
i=1134
while i<1260:
    GAMbf.iat[i, 1] = "K" #Male gender
    GAMbf.iat[i, 2] = "iw" #Western decendants
    i=i+1
i=1260
while i<1386:
    GAMbf.iat[i, 1] = "M"
    GAMbf.iat[i, 2] = "dw" #Non-western decendants
    i=i+1
i=1386
while i<1512:
    GAMbf.iat[i, 1] = "K"
    GAMbf.iat[i, 2] = "dw"
    i=i+1
        
i=1764
while i<1890:
    GAMbf.iat[i, 1] = "M"  #Female gender
    GAMbf.iat[i, 2] = "ix" #non-Western immigrants
    i=i+1
    
i=1890
while i<2006:
    GAMbf.iat[i, 1] = "K" #Female gender
    GAMbf.iat[i, 2] = "ix" #Non-Western immigrants
    i=i+1
    
    
i=2006
while i<2134:
    GAMbf.iat[i, 1] = "M"#Female gender
    GAMbf.iat[i, 2] = "dx" #Western decendants
    i=i+1
i=2134
while i<2268:
    GAMbf.iat[i, 1] = "K" #Female gender
    GAMbf.iat[i, 2] = "dx" #Non-Western decendants
    i=i+1

# In[5]: Cleans up historical data
GAMbf.drop(GAMbf.index[1512:1764],inplace=True) #removes unwanted data
GAMbf.drop(GAMbf.index[252:1008],inplace=True)#removes unwanted data
GAMbf.drop(["level_0"], axis=1 ,inplace=True)#removes unwanted data
GAMbf.index = pd.Index(range(1260),inplace=True)#Reindex


# In[6]: Shuffle around positions of the forecast data to be aligned with historical and merge
demo = GAMbf #Demo collects the entire population dataset - first step here is to collect old data
poptemp = pd.concat([FREMbf.iloc[0:126, 3:], FREMbf.iloc[630:756, 3:], FREMbf.iloc[126:252, 3:], FREMbf.iloc[756:882, 3:], FREMbf.iloc[378:504, 3:], FREMbf.iloc[1008:1134, 3:], FREMbf.iloc[252:378, 3:], FREMbf.iloc[882:1008, 3:], FREMbf.iloc[504:630, 3:],FREMbf.iloc[1134:, 3:] ], ignore_index=True)
#                   DA M                           DA K                     IW M                          IW K                DW M                      DW K                      IX M                        IX K                          dx M                     DX K
demo = pd.concat([demo, poptemp], axis=1, sort=False ) #Final population container

# In[7]: Viasual representation of the demographics


#Calculates age groups
demo15 = demo.loc[(0<=demo['age']) & (demo['age']<=14), '2008':'2060'].sum().to_frame().T
demo60 = demo.loc[(15<=demo['age']) & (demo['age']<=60), '2008':'2060'].sum().to_frame().T
demo64 = demo.loc[(61<=demo['age']) & (demo['age']<=64), '2008':'2060'].sum().to_frame().T
demo65 = demo.loc[(65<=demo['age']) & (demo['age']<=125), '2008':'2060'].sum().to_frame().T
demoage = pd.concat([demo15,demo60,demo64,demo65])
demoage.index =['0-14', '15-60', '60-64', '65+']
demoage.columns = np.arange(2008,2061,1)
demoages = demoage / demoage.sum()*100
#Plots age groups
fig = plt.figure()
plt.plot(demoages.iloc[0, :], label = '0-14')
plt.plot(demoages.iloc[1, :], label = '15-60')
plt.plot(demoages.iloc[2, :], label = '61-64')
plt.plot(demoages.iloc[3, :], label = '65+')
leg=plt.legend()
plt.xlim(2008,2060)
plt.show()


# In[8]: Data cleaning on employment rates
print(RAS200[RAS200["BEREGNING"]=='Beskæftigelsesfrekvens'])

RAS200.loc[RAS200.HERKOMST=="Personer med dansk oprindelse", 'HERKOMST'] = 'da'
RAS200.loc[RAS200.HERKOMST=="Indvandrere fra vestlige lande", 'HERKOMST'] = 'iw'
RAS200.loc[RAS200.HERKOMST=="Efterkommere fra vestlige lande", 'HERKOMST'] = 'dw'
RAS200.loc[RAS200.HERKOMST=="Indvandrere fra ikke-vestlige lande", 'HERKOMST'] = 'ix'
RAS200.loc[RAS200.HERKOMST=="Efterkommere fra ikke-vestlige lande", 'HERKOMST'] = 'dx'
RAS200.loc[RAS200.KØN=="Kvinder", 'KØN'] = 'K'
RAS200.loc[RAS200.KØN=="Mænd", 'KØN'] = 'M'
RAS200.loc[RAS200.BEREGNING=="Beskæftigelsesfrekvens", 'BEREGNING'] = 'besk'
RAS200.loc[RAS200.BEREGNING=="Erhvervsfrekvens", 'BEREGNING'] = 'uab'



# In[9]: Forecasting actual employment, holding frequencies constant from 2017

employ = pd.DataFrame(columns = ["gender", "origin", "age"]) #container for employment data
employ = pd.concat([employ, pd.DataFrame(columns = np.arange(2008,2061,1))], axis=1) #creating relevant time headers

employ["gender"] = demo["gender"]
employ["origin"] = demo["origin"]
employ["age"] = demo["age"]

employ.loc[(15>= employ["age"]), 3:] = 0 #We do not support childlabour

employ.loc[(employ["age"] = 16) & (employ["age"] = 17) & (employ["gender"] = 'M') & (employ["origin"] = 'da') , 3:12] = demo * RAS200.loc[(RAS200['TID'] = 2008) & (RAS200['ALDER'] = '16-17 år') & (RAS200['HERKOMST'] == 'da') & (RAS200['KØN'] == 'M') & (RAS200['BEREGNING'] == 'besk'), 3:12]/100






















