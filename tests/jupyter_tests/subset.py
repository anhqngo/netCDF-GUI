#!/usr/bin/env python
# coding: utf-8

# In[41]:


import xarray as xr


# In[55]:


ds = xr.open_dataset("../datasets/ds_1_point.nc", decode_times=False)
ds


# In[147]:


import numpy as np
test = (np.Inf, -np.Inf, np.Inf, -np.Inf)
(lat_max, lat_min, lon_max, lon_min) = test

temp =  ds.where((
            (ds.coords['lat'] >= 4).all() & 
            (360 >= ds.coords['lon']).all()
), drop=True)
temp


# In[125]:


x = ds['observation'].values
x = x[~np.isnan(x)]
(x >= 0).all()


# In[83]:


da.where(((lat_max >= da.coords['lat']).all() & (lon_max >= da.coords['lon']).all()))


# In[84]:


da


# In[86]:


da['variable']


# In[90]:


da.coords


# In[97]:


da.loc[:,[2,3]]


# In[98]:


a = np.array([2,3,4,5,6,7,7])


# In[130]:


(ds.data_vars['observation'] >= 0).all()


# In[139]:


min(temp['observation'].values)


# In[149]:


a[(1,2,6),]


# In[150]:


lon_max


# In[157]:


np.where((ds['lon']<=lon_max & ds['lat']>=20))


# In[152]:


index = np.array([1,2])
a[index,]


# In[171]:


a = np.array([1, 2, 3, 1, 2, 3])
np.where(
    (a>2)
#     & (a<5).any()
)[0]


# In[173]:


df = da.to_dataframe(name='frame')


# In[174]:


df


# In[179]:


df.where(df.lat > 20).where(df.lon > 100)


# In[189]:


temp = ds.where(ds['lat']>20,drop=True)


# In[190]:


temp


# In[191]:


temp = temp.where(temp['lon'] < 140, drop=True)


# In[192]:


temp


# In[195]:


A = [
    max(ds['lon'].values),
    max(ds['lat'].values),
    min(ds['lon'].values),
    min(ds['lat'].values)
]


# In[196]:


A


# In[ ]:




