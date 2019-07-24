#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import xarray as xr
from netCDF4 import Dataset


# In[5]:


ds = xr.open_dataset("../datasets/proposed_standard/salinity_4.nc",decode_times=False)
ds


# In[6]:


tim = xr.open_dataset("../../../Downloads/SIParCS-19/netCDF_files/tim_obs4.nc",decode_times=False)
tim


# In[8]:


ds['observations'].values = tim['observations'].values
ds['observations'].values


# In[6]:


ds.to_netcdf(format="")


# In[6]:


rootgrp.groups


# In[10]:


ds2 = xr.open_dataset("../datasets/proposed_standard/soil_salinity_standard.nc",group="/Europe",decode_times=False)
ds2


# In[26]:


def walktree(top):
    values = top.groups.values()
    yield values
    for value in top.groups.values():
        for children in walktree(value):
            yield children

groupList=[]
for children in walktree(rootgrp):
    for child in children:
        print(child.name)
        groupList.append(child.name)

print(groupList)


# ### See which group(s) an observation is in:

# ### Plot all observations within that group:

# In[26]:


import random
for i in np.sort(random.sample(range(232323), 100000)):
    print(str(i)+", ")


# In[ ]:





# In[ ]:




