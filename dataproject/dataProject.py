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


GAMbf = requests.get('https://api.statbank.dk/v1/data/FOLK1E/CSV?delimiter=Semicolon&K%C3%98N=1%2C2&Tid=*&Herkomst=1%2C24%2C25%2C34%2C35&ALDER=*').content
GAMbf = pd.read_csv(io.StringIO(GAMbf.decode('utf-8')),decimal=",",sep=";")


FREMbf = requests.get('https://api.statbank.dk/v1/data/FRDK118/CSV?HERKOMST=*&K%C3%98N=*&ALDER=*&Tid=*').content
FREMbf = pd.read_csv(io.StringIO(FREMbf.decode('utf-8')),decimal=",",sep=";")


# In[3]: Data cleaning on hisotrical population
GAMbf = GAMbf.loc[GAMbf.TID.str[-1]=='1'] #Data is in quaters - we use the first quarter each year 
GAMbf.TID = GAMbf.TID.str[0:4] #creates a list of year without quarter indicator at the end (2008k1 -> 2008)
GAMbf = GAMbf[GAMbf.ALDER !='I alt'] #drops observations containing the sum across ages.
GAMbf.loc[GAMbf.HERKOMST=="Personer med dansk oprindelse", 'HERKOMST'] = 'da'
GAMbf.loc[GAMbf.HERKOMST=="Indvandrere fra vestlige lande", 'HERKOMST'] = 'iw'
GAMbf.loc[GAMbf.HERKOMST=="Indvandrere fra ikke-vestlige lande", 'HERKOMST'] = 'ix'
GAMbf.loc[GAMbf.HERKOMST=="Efterkommere fra vestlige lande", 'HERKOMST'] = 'dw'
GAMbf.loc[GAMbf.HERKOMST=="Efterkommere fra ikke-vestlige lande", 'HERKOMST'] = 'dx'
GAMbf.loc[GAMbf.KØN=="Mænd", 'KØN'] = 'M'
GAMbf.loc[GAMbf.KØN=="Kvinder", 'KØN'] = 'K'
GAMbf.rename(columns = {'KØN':'gender', 'TID':'year','HERKOMST':'origin','ALDER':'age', 'INDHOLD':'pop'}, inplace = True)
GAMbf["age"] = GAMbf["age"].astype(str).str.split(" ", 1, expand=True) #picks up the integer part(before first space) of the age variable.
GAMbf["age"] = GAMbf["age"].astype(int)
GAMbf.pop = GAMbf.loc[:,"pop"].astype(float) #converts frequencies to floats from strings

# In[4]: Creates indexes to match origin and gender in forecast data
FREMbf.loc[FREMbf.HERKOMST=="Personer med dansk oprindelse", 'HERKOMST'] = 'da'
FREMbf.loc[FREMbf.HERKOMST=="Indvandrere fra vestlige lande", 'HERKOMST'] = 'IW'
FREMbf.loc[FREMbf.HERKOMST=="Indvandrere fra ikke-vestlige lande", 'HERKOMST'] = 'IX'
FREMbf.loc[FREMbf.HERKOMST=="Efterkommere fra vestlige lande", 'HERKOMST'] = 'dw'
FREMbf.loc[FREMbf.HERKOMST=="Efterkommere fra ikke-vestlige lande", 'HERKOMST'] = 'dx'
FREMbf.loc[FREMbf.KØN=="Mænd", 'KØN'] = 'M'
FREMbf.loc[FREMbf.KØN=="Kvinder", 'KØN'] = 'K'
FREMbf.rename(columns = {'KØN':'gender', 'TID':'year','HERKOMST':'origin', 'ALDER':'age', 'INDHOLD':'pop'}, inplace = True)
FREMbf["age"] = FREMbf["age"].astype(str).str.split(" ", 1, expand=True) #picks up the integer part(before first space) of the age variable.
FREMbf["age"] = FREMbf["age"].astype(int)
FREMbf.pop = FREMbf.loc[:,"pop"].astype(float) #converts frequencies to floats from strings

# In[8]: Data cleaning on employment rates
RAS200.loc[RAS200.HERKOMST=="Personer med dansk oprindelse", 'HERKOMST'] = 'da'
RAS200.loc[RAS200.HERKOMST=="Indvandrere fra vestlige lande", 'HERKOMST'] = 'iw'
RAS200.loc[RAS200.HERKOMST=="Indvandrere fra ikke-vestlige lande", 'HERKOMST'] = 'ix'
RAS200.loc[RAS200.HERKOMST=="Efterkommere fra ikke-vestlige lande", 'HERKOMST'] = 'dx'
RAS200.loc[RAS200.KØN=="Kvinder", 'KØN'] = 'K'
RAS200.loc[RAS200.HERKOMST=="Efterkommere fra vestlige lande", 'HERKOMST'] = 'dw'
RAS200.loc[RAS200.KØN=="Mænd", 'KØN'] = 'M'
RAS200.loc[RAS200.BEREGNING=="Beskæftigelsesfrekvens", 'BEREGNING'] = 'besk'
RAS200.loc[RAS200.BEREGNING=="Erhvervsfrekvens", 'BEREGNING'] = 'uab'
RAS200 = RAS200.drop(columns = ['OMRÅDE'])
RAS200.rename(columns = {'KØN':'gender', 'TID':'year','HERKOMST':'origin', 'ALDER':'age', 'INDHOLD':'frequency', "BEREGNING":'activ'}, inplace = True)


# In[9]: Data cleaning on employment rates
freq_temp = RAS200 #Creates a tempoary frequency container - ensures that we do not alter original data
alder = freq_temp["age"].astype(str).str.split("-", expand=True) #Splits "ALDER" (example: 16-17 år) collumn into two collumns by thedelimiter "-".
alder[1] = alder[1].astype(str).str.split(" ", expand=True) #The second created collumn has "år" in the end of the string - we only keep the integer part by keeping the string priror to the delimiter " ".

alder = alder.astype(float) #converts strings to floats (could also be integer)

freqalder =  pd.DataFrame() #creates a container for the interval of ages - used for loop later to create a collumn of ages from 16 to 64. 
for i,j in zip(alder.iloc[:,1], alder.iloc[:,0]):
    app = pd.Series(i-j)
    freqalder = freqalder.append(app, ignore_index=True)

freq =  pd.DataFrame() #container for final data on employmentrates
age_temp = pd.DataFrame() #temporary container to create a list of ages 
p=0
for i in freqalder.iloc[:,0]: #We want to iterate as long as we have age groups
    if i ==1: #if the age group contains two ages (i=17-16 ==1 )
        freq = freq.append(RAS200.iloc[p,:]) #copies RAS-data so, for instance age 16 and 17 have the same gender, origin and frequency as the age group 16-17
        freq = freq.append(RAS200.iloc[p,:]) #We do the same for the next age in the interval 
        age_temp = age_temp.append(pd.Series(alder.iloc[p,0]), ignore_index=True) #sets the age_temp equal to the first age of the interval
        age_temp = age_temp.append(pd.Series(alder.iloc[p,0]+1), ignore_index=True) #Adds 1 to the first age of the interval
        p=p+1
    else: #If the interval contains 5 ages
        freq = freq.append(RAS200.iloc[p,:])
        freq = freq.append(RAS200.iloc[p,:])
        freq = freq.append(RAS200.iloc[p,:])
        freq = freq.append(RAS200.iloc[p,:])
        freq = freq.append(RAS200.iloc[p,:])
        age_temp = age_temp.append(pd.Series(alder.iloc[p,0]), ignore_index=True)
        age_temp = age_temp.append(pd.Series(alder.iloc[p,0]+1), ignore_index=True)
        age_temp = age_temp.append(pd.Series(alder.iloc[p,0]+2), ignore_index=True)
        age_temp = age_temp.append(pd.Series(alder.iloc[p,0]+3), ignore_index=True)
        age_temp = age_temp.append(pd.Series(alder.iloc[p,0]+4), ignore_index=True)
        p=p+1 
freq.index = range(len(freq)) #Append keeps the old index - We want to concatenate later using a different index.
age_temp.rename(columns = {0:"age"}, inplace=True) #rename the collum to "age" 
freq = pd.concat([freq, age_temp], axis=1)

# In[10]: Forecasting employment

freq_besk = freq[freq["BEREGNING"] == 'besk']



















