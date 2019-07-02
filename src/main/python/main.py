# Miscelleneous packages
import sys
import numpy as np

# PyQt Modules
from PyQt5.QtWidgets import *
from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property

# UI Classes
from ui.main_window import Ui_MainWindow
from ui.subset_location_dialog import Ui_subset_location_dialog

# NetCDF packages
import xarray as xr

# Plotting modules
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# MetPy packages
import metpy.calc as mpcalc
from metpy.testing import get_test_data
from metpy.units import units


TEST = 1
TEST_FILE = "/Users/jngo/netCDF-GUI/tests/datasets/ds_1_point.nc"


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
        self.actionSave.triggered.connect(self.get_ds_subset)
        # TODO: connect to the right slot
        version = self.ctx.build_settings['version']
        self.setWindowTitle(
            "DART Plotting Tool v." + version)

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

    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "",
            "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            self.debugContents.append("Save file: {}".format(fileName))
        # TODO: do somethign with the save file function. It might not be
        # needed

    def read_file(self, fileName):
        """
        Display the general information about the dataset and list all the
        variables on the GUI
        """
        self.ds = xr.open_dataset(fileName, decode_times=False)
        self.headerContents.setText(
            "File name: {}".format(fileName) + "\n" + str(self.ds))
        self.variableList.addItems(list(self.ds.data_vars))
        self.variableList.itemDoubleClicked.connect(self.show_item)

    def show_item(self, item):
        selected_var = item.text()
        self.debugContents.append("Selected variable: {}".format(selected_var))
        self.scatter_plot(selected_var)

    def scatter_plot(self, selected_var):
        """
        Display a basic geo scatter plot of observation data
        """
        temp = self.get_ds_subset()
        try:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
            ax.stock_img()
            # sc = plt.scatter(self.ds['lon'].values, self.ds['lat'].values,
            #                  c=self.ds[selected_var].values)
            sc = plt.scatter(temp['lon'].values, temp['lat'].values,
                             c=temp[selected_var].values)

            plt.colorbar(sc)
            plt.title("{} Data".format(selected_var.capitalize()))
            plt.show()
            self.debugContents.append("Scatter Plot of {}".format(
                selected_var.capitalize()))
        except Exception as e:
            self.debugContents.append("Error: {}".format(str(e)))

    def get_observation_type(self):
        pass
        # TODO: rewrite the function

    def get_ds_subset(self):
        # self.dialog = SubsetLocationDialog()
        self.dialog.exec_()

        lon_max = self.dialog.lon_max_input.text()
        lon_min = self.dialog.lon_min_input.text()
        lat_max = self.dialog.lat_max_input.text()
        lat_min = self.dialog.lat_min_input.text()

        lon_max = string_to_float_max(lon_max)
        lon_min = string_to_float_min(lon_min)
        lat_max = string_to_float_max(lat_max)
        lat_min = string_to_float_min(lat_min)

        self.ds_temp = self.ds.where((
            (lat_max >= self.ds.coords['lat']).all() &
            (lat_min <= self.ds.coords['lat']).all() &
            (lon_max >= self.ds.coords['lon']).all() &
            (lon_min <= self.ds.coords['lon']).all()), drop=True)

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


if __name__ == '__main__':
    APPCTXT = AppContext()
    EXIT_CODE = APPCTXT.run()
    sys.exit(EXIT_CODE)
