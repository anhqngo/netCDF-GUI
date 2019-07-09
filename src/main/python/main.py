# Miscelleneous packages
import sys
import numpy as np
import itertools

# PyQt Modules
from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog
from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property

# UI Classes
from ui.main_window import Ui_MainWindow
from ui.subset_location_dialog import Ui_subset_location_dialog

# NetCDF packages
import xarray as xr
from netCDF4 import Dataset

# Matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import LineCollection, PolyCollection

# Cartopy
import cartopy.feature
from cartopy.mpl.patch import geos_to_path
import cartopy.crs as ccrs

# MetPy packages
# import metpy.calc as mpcalc
# from metpy.testing import get_test_data
# from metpy.units import units


TEST = 0
TEST_FILE = "/Users/jngo/netCDF-GUI/tests/datasets/proposed_standard/salinity_4.nc"


class AppContext(ApplicationContext):
    def run(self):
        self.main_window.show()
        return self.app.exec_()

    @cached_property
    def main_window(self):
        return MainWindow(self)


class SubsetLocationDialog(QDialog, Ui_subset_location_dialog):
    def __init__(self):
        super(SubsetLocationDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Subset Location Dialog")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, ctx):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.ctx = ctx
        
        self.dialog = SubsetLocationDialog()

        self.actionOpen.triggered.connect(self.open_file_dialog)

        version = self.ctx.build_settings['version']
        self.setWindowTitle(
            "DART Plotting Tool v." + version)
        self.obsIndexPush.clicked.connect(self.show_parent_groups)

        if TEST == 1:
            self.debugContents.append("Open file: {}".format(TEST_FILE))
            self.read_file(TEST_FILE)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;NetCDF Files (*.nc)", options=options)
        if fileName:
            self.debugContents.append("Open file: {}".format(fileName))
            self.read_file(fileName)
        else:
            self.debugContents.append("Cannot open file")

    def read_file(self, fileName):
        """
        Display the general information about the dataset and list all the
        variables on the GUI
        """
        self.ds = xr.open_dataset(fileName, decode_times=False)
        self.rootgrp = Dataset(fileName, "r", format="NETCDF4")
        self.headerContents.setText(
            "File name: {}".format(fileName) + "\n" + str(self.ds))
        self.variableList.addItems(list(self.ds.data_vars))
        self.variableList.itemDoubleClicked.connect(self.show_item)

        self.groupList = []
        for children in walktree(self.rootgrp):
            for child in children:
                self.groupList.append(child.name)
        self.groupContents.addItems(self.groupList)

    def show_item(self, item):
        selected_var = item.text()
        self.debugContents.append("Selected variable: {}".format(selected_var))
        self.scatter_plot(selected_var)
        self.scatter_plot_3d(selected_var)

    def show_parent_groups(self):
        try:
            obs_index = int(self.obsIndexInput.text())
        except:
            print("Must be an integer")
        print(obs_index)
        self.ds = xr.open_dataset(TEST_FILE, decode_times=False)
        _list_of_groups = self.ds['list_of_groups'].values[obs_index]
        _list_of_groups = np.where(_list_of_groups>=0)[0]
        self.parentGroupList.setText("")
        if len(_list_of_groups) == 0:
            self.parentGroupList.setText("No groups available")
        else:
            for groupIndex in _list_of_groups:
                if groupIndex < 0:
                    continue
                print(groupIndex)
                self.parentGroupList.append(self.groupList[groupIndex])

    def scatter_plot(self, selected_var):
        """
        Display a basic geo scatter plot of observation data
        """

        self.debugContents.append("Processing scatter plot 2D...")
        ds_subset = self.get_ds_subset()

        try:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
            ax.stock_img()
            # sc = plt.scatter(self.ds['lon'].values, self.ds['lat'].values,
            #                  c=self.ds[selected_var].values)
            sc = plt.scatter(ds_subset['lon'].values, ds_subset['lat'].values,
                             c=ds_subset[selected_var].values.T[0])

            plt.colorbar(sc)

            # TODO: the following two lines don't seem to do anything
            plt.xlabel("X Label")
            plt.ylabel("Y label")

            plt.title("{} Data".format(selected_var.capitalize()))
            plt.show()
            self.debugContents.append("Scatter Plot of {}".format(
                selected_var.capitalize()))

        except Exception as e:
            self.debugContents.append("Error: {}".format(str(e)))

    def scatter_plot_3d(self, selected_var):
        """
        Display 3D scatter plot of selected variable
        """

        self.debugContents.append("Processing scatter plot 3D...")
        ds_subset = self.get_ds_subset()

        try:
            fig = plt.figure()
            ax = Axes3D(fig, xlim=[-180, 180], ylim=[-90, 90])
            ax.set_zlim(bottom=0)

            def concat(iterable): return list(
                itertools.chain.from_iterable(iterable))

            target_projection = ccrs.PlateCarree()

            feature = cartopy.feature.NaturalEarthFeature(
                'physical', 'land', '110m')
            geoms = feature.geometries()

            geoms = [target_projection.project_geometry(geom, feature.crs)
                     for geom in geoms]

            paths = concat(geos_to_path(geom) for geom in geoms)

            COLOR = True
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

            sc = ax.scatter(
                ds_subset['lon'].values,
                ds_subset['lat'].values,
                ds_subset['vertical'].values,
                c=ds_subset[selected_var].values.T[0],
                alpha=0.5)
            plt.colorbar(sc)
            ax.add_collection3d(lc)
            ax.add_collection3d(sc)

            ax.set_xlabel('degrees_east')
            ax.set_ylabel('degrees_north')
            ax.set_zlabel('Height')

            plt.title("{} Data".format(selected_var.capitalize()))
            plt.show()

            self.debugContents.append("Scatter Plot 3D of {}".format(
                selected_var.capitalize()))
        except Exception as e:
            self.debugContents.append("Error: {}".format(str(e)))

    def get_observation_type(self):
        pass
        # TODO: rewrite the function

    def get_ds_subset(self):
        # self.dialog = SubsetLocationDialog()
        self.dialog.exec_()

        # TODO: make the code below more compact
        lon_max = self.dialog.lon_max_input.text()
        lon_min = self.dialog.lon_min_input.text()
        lat_max = self.dialog.lat_max_input.text()
        lat_min = self.dialog.lat_min_input.text()

        lon_max = string_to_float_max(lon_max)
        lon_min = string_to_float_min(lon_min)
        lat_max = string_to_float_max(lat_max)
        lat_min = string_to_float_min(lat_min)

        self.ds_temp = self.ds.where(
            lat_max >= self.ds.coords['lat'], drop=True)
        self.ds_temp = self.ds_temp.where(
            lat_min <= self.ds_temp.coords['lat'], drop=True)
        self.ds_temp = self.ds_temp.where(
            lon_max >= self.ds_temp.coords['lon'], drop=True)
        self.ds_temp = self.ds_temp.where(
            lon_min <= self.ds_temp.coords['lon'], drop=True)

        return self.ds_temp


def string_to_float_max(floatString):
    if floatString:
        return float(floatString)
    else:
        return np.Inf


def string_to_float_min(floatString):
    if floatString:
        return float(floatString)
    else:
        return -np.Inf


def walktree(top):
    """
    The function walktree is a Python generator that is used to walk the directory tree.
    """
    values = top.groups.values()
    yield values
    for value in top.groups.values():
        for children in walktree(value):
            yield children


if __name__ == '__main__':
    APPCTXT = AppContext()
    EXIT_CODE = APPCTXT.run()
    sys.exit(EXIT_CODE)
