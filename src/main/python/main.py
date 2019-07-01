# Miscelleneous packages
import sys
import random

# PyQt Modules
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property

# UI Classes
from ui.main_window import Ui_MainWindow

# NetCDF packages
import netCDF4
import xarray as xr

# Plotting modules
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from pyqtgraph import PlotWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pyqtgraph as pg

# MetPy packages
import metpy.calc as mpcalc
from metpy.testing import get_test_data
from metpy.units import units

# Scientific packages
import numpy as np
import pandas as pd

TEST = 1
TEST_FILE = "/Users/jngo/netCDF-GUI/tests/datasets/ds_1_point.nc"


class AppContext(ApplicationContext):
    def run(self):
        self.main_window.show()
        return self.app.exec_()

    @cached_property
    def main_window(self):
        return MainWindow(self)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, ctx):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.ctx = ctx

        self.actionOpen.triggered.connect(
            self.open_file_dialog)
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

    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "",
            "All Files (*);;Text Files (*.txt)", options=options)
        
    def read_file(self, fileName):
        """ Display the general information about the dataset and list all the
        variables
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
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax.stock_img()
        sc = plt.scatter(self.ds['lon'].values, self.ds['lat'].values,
                         c=self.ds[selected_var].values)
        plt.colorbar(sc)
        plt.show()

    def get_observation_type(self):
        pass
        
        
if __name__ == '__main__':
    APPCTXT = AppContext()
    EXIT_CODE = APPCTXT.run()
    sys.exit(EXIT_CODE)
