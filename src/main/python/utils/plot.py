import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def scatter_plot(ds):
    ds = xr.open_dataset('TODO', decode_times=False)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.stock_img()
    ax.coastlines()

    sc = plt.scatter(ds['lon'].values, ds['lat'].values,
                     c=ds['observation'].values)
    plt.colorbar(sc)
    plt.show()
