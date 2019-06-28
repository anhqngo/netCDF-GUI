#!/usr/bin/env python
# coding: utf-8

# In[23]:


# NetCDF packages
import netCDF4
from netCDF4 import Dataset
import xarray
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# MetPy packages
import metpy.calc as mpcalc
from metpy.testing import get_test_data
from metpy.units import units


# In[3]:


ds = xr.open_dataset('../datasets/ds_1.nc', decode_times=False)


# In[16]:


vars = ds.data_vars


# In[17]:


vars


# In[18]:


type(vars)


# In[21]:


for i in vars:
    print(i)
    print(type(i))


# In[22]:


type(vars)


# In[25]:


rootgrp = Dataset('../datasets/ds_1.nc', "r", format="NETCDF4")


# In[27]:


type(rootgrp)


# In[28]:


type(ds)


# In[ ]:




