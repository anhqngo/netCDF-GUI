#!/usr/bin/env python
# coding: utf-8

# In[1]:


# NetCDF packages
import netCDF4
from netCDF4 import Dataset
import xarray
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from mpl_toolkits import mplot3d

# MetPy packages
import metpy.calc as mpcalc
from metpy.testing import get_test_data
from metpy.units import units


# In[2]:


ds = xr.open_dataset('../datasets/ds_1_point.nc',decode_times=False)
ds


# In[3]:


lon, lat, vert, time = ds['lon'].values, ds['lat'].values, ds['vertical'].values, ds['time'].values
observation = ds['observation'].values


# In[4]:


`


# In[28]:


typeFile = xr.open_dataset("../../type.nc", decode_times=False)


# In[29]:


typeFile['obs'].values['wind']


# In[6]:


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


# In[12]:


observation


# In[7]:


from mpl_toolkits import *


# In[6]:





# In[4]:


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap

map = Basemap()

fig = plt.figure()
ax = Axes3D(fig)

'''
ax.azim = 270
ax.elev = 90
ax.dist = 5
'''

ax.add_collection3d(map.drawcoastlines(linewidth=0.25))
ax.add_collection3d(map.drawcountries(linewidth=0.35))

plt.show()


# In[ ]:




