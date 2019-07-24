#!/usr/bin/env python
# coding: utf-8

# In[4]:


import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


# In[5]:


ds = xr.open_dataset('comparison_tools_CF.nc',decode_times=False)


# In[6]:


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.stock_img()
ax.coastlines()

sc = plt.scatter(ds['lon'].values, ds['lat'].values, c=ds['observation'].values)
plt.colorbar(sc)
plt.show()


# ## Extract first 1000 observations

# In[4]:


new = xr.open_dataset('comparison_tools_CF_1000.nc')
new


# In[5]:


new['time'] = ds['time'][:1000]
new['lon'] = ds['lon'][:1000]
new['lat'] = ds['lat'][:1000]
new['alt'] = ds['alt'][:1000]
new['observation'] = ds['observation'][:1000]


# In[6]:


new


# In[7]:


new.to_netcdf('new_1000.nc')


# In[ ]:




