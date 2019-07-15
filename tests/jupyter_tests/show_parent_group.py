#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import xarray as xr
from netCDF4 import Dataset


# In[3]:


ds = xr.open_dataset("../datasets/proposed_standard/salinity_4.nc",decode_times=False)


# In[5]:


ds['list_of_groups'].values


# In[10]:


ds['observations'].attrs


# In[11]:


a = np.array([1,2,3])


# In[19]:


np.where(a>1)[0]m


# In[21]:


from jupyter_core.paths import jupyter_config_dir
jupyter_dir = jupyter_config_dir()  # C:\users\<user_name>\.jupyter on my machine
jupyter_dir


# In[ ]:




