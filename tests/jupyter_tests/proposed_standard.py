#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import xarray as xr
from netCDF4 import Dataset


# In[43]:


ds = xr.open_dataset("../datasets/proposed_standard/salinity_4.nc",decode_times=False)
ds


# In[44]:


rootgrp = Dataset("../datasets/proposed_standard/salinity_4.nc", "r", format="NETCDF4")
rootgrp.groups
rootgrp['/Purple/obs_id'][:].compressed() # return only valid entries from numpy masked array


# In[63]:


orange = rootgrp['/Orange/obs_id'][:].compressed()
apple = rootgrp['/Apple/obs_id'][:].compressed()
purple = rootgrp['/Purple/obs_id'][:].compressed()

for obs in range(232323):
    if obs in orange:
        ds['list_of_groups'].values[obs] = np.append(ds['list_of_groups'].values[obs],0)
    if obs in apple:
        ds['list_of_groups'].values[obs] = np.append(ds['list_of_groups'].values[obs],1)
    if obs in purple:
        ds['list_of_groups'].values[obs] = np.append(ds['list_of_groups'].values[obs],2)
    if len(ds['list_of_groups'].values[obs]) == 0:
        print("_,")
    else:
        print(set(ds['list_of_groups'].values[obs]), ",")


# In[62]:


a = np.array()
if a:
    print(2)


# In[58]:


print(2,"hello")


# In[47]:


ds.to_netcdf(path="blah2.nc",engine="netcdf4")


# In[8]:


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


# ### See which group(s) an observation is in:

# ### Plot all observations within that group:

# In[66]:


rootgrp = Dataset("../datasets/proposed_standard/salinity_4.nc", "r", format="NETCDF4")
rootgrp.groups


# In[67]:


orange


# In[77]:


rootgrp['/Purple/obs_id'][:].compressed()


# In[78]:


test_arr = np.array([0,1])


# In[80]:


ds['lat'].values[test_arr]


# In[ ]:




