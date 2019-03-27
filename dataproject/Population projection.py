#!/usr/bin/env python
# coding: utf-8

# ## Labour market projections
# This code produces a projection of the Danish labour market from 2017 to 2059 using The Register-based Labour Force Statistics (RAS) and the population projection from Statistics Denmark. The code is structured in four main elements:
# 
# 1. Data collection
# 2. Base projection
# 3. Indexing pension age to life expectancy
# 4. Results
# 
# The basic principle of the projection is:
#  $$A = \sum B$$
# 

# ## Packages
# We'll need some packages to do some dirty work for us.

# In[61]:


import requests        # Needed to download the data from Statistics Denmark's API
import io              # Also needed to download the data from Statistics Denmark's API
import pandas as pd    # Pandas - because everybody loves pandas


# ## 1. Data
# Now we are ready to stream some data! We'll need the tables RAS200, XX, YY and ZZ.

# In[73]:


## RAS200 - 
url_RAS200 = 'https://api.statbank.dk/v1/data/RAS200/CSV?valuePresentation=Value&delimiter=Semicolon&BEREGNING=*&TID=2017&ALDER=16-17%2C18-19%2C20-24%2C25-29%2C30-34%2C35-39%2C40-44%2C45-49%2C50-54%2C55-59%2C60-64&HERKOMST=10%2C24%2C25%2C34%2C35&K%C3%98N=M%2CK&OMR%C3%85DE=000'
RAS200 = requests.get(url_RAS200).content
RAS200 = pd.read_csv(io.StringIO(RAS200.decode('utf-8')),sep=";")

## XX


# The next step is to define some variables, which we can use for our projections!
# 
# * Gender
# * Age
# * Origin
# * Activ
# * Freq
# 
# 
# 

# In[ ]:





# In[ ]:





# In[ ]:




