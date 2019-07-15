"""This module contains helper functions for plotting the dataset.
The features include: scatter plot 3D, time series plot, and DART QC plot.
"""

import itertools
import numpy as np

# Plotting library imports
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection
from mpl_toolkits.mplot3d import Axes3D

import seaborn as sns

import cartopy.feature
from cartopy.mpl.patch import geos_to_path
import cartopy.crs as ccrs

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def geo_3d_plot(dataset, variable):
    """
    Display 3D scatter plot of a variable within a specific group in a dataset
    """
    fig = plt.figure()
    sns.set()
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

    color = True
    if color:
        polys = concat(path.to_polygons() for path in paths)
        line_collection = PolyCollection(polys, edgecolor='black',
                                         facecolor='green', closed=False)
    else:
        segments = []
        for path in paths:
            vertices = [vertex for vertex, _ in path.iter_segments()]
            vertices = np.asarray(vertices)
            segments.append(vertices)
        line_collection = LineCollection(segments, color='black')
    ax.add_collection3d(line_collection)

    try:
        scatter_plot = ax.scatter(
            dataset['lon'].values,
            dataset['lat'].values,
            dataset['vertical'].values,
            c=dataset[variable].values.T[0],
            s=1,
            alpha=0.5)
    except BaseException:
        # TODO: need to standardize how we store the variables. This case is
        # only executed if we are plotting 1-D variables. This case won't work
        # if we decide to implement the obs variable to have (obs x copy)
        # dimension
        scatter_plot = ax.scatter(
            dataset['lon'].values,
            dataset['lat'].values,
            dataset['vertical'].values,
            c=dataset[variable].values,
            s=1,
            alpha=0.5)

    plt.colorbar(scatter_plot)
    ax.add_collection3d(scatter_plot)

    ax.set_zlim(0, max(dataset['vertical'].values) * 1.5)
    ax.set_xlabel('degrees_east')
    ax.set_ylabel('degrees_north')
    ax.set_zlabel('Height')
    plt.title("{} Data".format(variable.capitalize()))
    plt.show()


def time_series_qc_plot(dataset):
    """Display time series of quality control
    """
    fig = plt.figure(
        num=None,
        figsize=(
            8,
            6),
        dpi=80,
        facecolor='w',
        edgecolor='k')
    sns.set()
    # Filter out invalid qc values:
    temp = dataset.where(dataset['qc'] < 8, drop=True)
    plt.plot_date(x=temp['time'], xdate=True,
                  y=temp['qc'].values,
                  markerfacecolor="None", ms=5, alpha=0.05)
    plt.title("QC Values Time Series")
    plt.ylabel("QC Values")
    plt.xlabel("Time")
    plt.ylim(-0.1, 7.1)
    plt.show()


def qc_observations_plot(dataset):
    """Display count of observation corresponding to each qc value

    :param dataset: Dataset returned from main.get_dataset_subset()
    :type dataset: xarray.Dataset
    """
    plt.figure(figsize=(4, 3))
    sns.set()
    temp = dataset.where(dataset['qc'] < 8, drop=True)
    try:
        sns.countplot(y=temp['qc'].values.T[0], order=[7, 6, 5, 4, 3, 2, 1, 0])
    except KeyError:
        sns.countplot(y=temp['qc'].values, order=[7, 6, 5, 4, 3, 2, 1, 0])
    plt.title("Distribution of DART Quality Control Values")
    plt.xlabel('Number of Observations')
    plt.ylabel('DART QC Values')
    plt.show()
