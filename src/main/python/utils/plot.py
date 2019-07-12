"""This module contains helper functions for plotting the dataset.
The features include: scatter plot 3D, time series plot, and DART QC plot.
"""

import itertools
import numpy as np
import xarray as xr

# Plotting library imports
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection
from mpl_toolkits.mplot3d import Axes3D


import cartopy.feature
from cartopy.mpl.patch import geos_to_path
import cartopy.crs as ccrs


def geo_3d_plot(dataset, variable, obs_index_array):
    """
    Display 3D scatter plot of a variable within a specific group in a dataset
    """
    fig = plt.figure()
    ax = Axes3D(fig, xlim=[-180, 180], ylim=[-90, 90])
    ax.set_zlim(bottom=0)

    def concat(iterable):
        return list(itertools.chain.from_iterable(iterable))
    target_projection = ccrs.PlateCarree()
    feature = cartopy.feature.NaturalEarthFeature(
        'physical', 'land', '110m')
    geoms = feature.geometries()
    geoms = [target_projection.project_geometry(geom, feature.crs)
             for geom in geoms]
    paths = concat(geos_to_path(geom) for geom in geoms)

    COLOR = False
    if COLOR:
        polys = concat(path.to_polygons() for path in paths)
        lc = PolyCollection(polys, edgecolor='black',
                            facecolor='green', closed=False)
    else:
        segments = []
        for path in paths:
            vertices = [vertex for vertex, _ in path.iter_segments()]
            vertices = np.asarray(vertices)
            segments.append(vertices)
        lc = LineCollection(segments, color='black')
    ax.add_collection3d(lc)

    sc = ax.scatter(
        dataset['lon'].values[obs_index_array],
        dataset['lat'].values[obs_index_array],
        dataset['vertical'].values[obs_index_array],
        c=dataset[variable].values.T[0][obs_index_array],
        s=1,
        alpha=0.5)
    plt.colorbar(sc)
    ax.add_collection3d(sc)

    # TODO: consider fixing the bounds
    ax.set_zlim(0, max(dataset['vertical'].values) * 1.5)
    ax.set_xlabel('degrees_east')
    ax.set_ylabel('degrees_north')
    ax.set_zlabel('Height')
    plt.title("{} Data".format(variable.capitalize()))
    plt.show()


def time_series_qc_plot(dataset, obs_index_array):
    dataset = xr.decode_cf(dataset, decode_times=True)
    fig = plt.figure(
        num=None,
        figsize=(
            8,
            6),
        dpi=80,
        facecolor='w',
        edgecolor='k')
    # Filter out invalid qc values:
    temp = dataset.where(8 > dataset['qc'], drop=True)
    plt.plot_date(x=temp['time'], y=temp['qc'].values, xdate=True,
                  markerfacecolor="None", ms=5, alpha=0.05)
    plt.title("QC Values Time Series")
    plt.ylabel("QC Values")
    plt.xlabel("Time")
    plt.show()


def qc_observations_plot(dataset, variable, obs_index_array):
    pass
