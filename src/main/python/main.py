import sys

# PyQt Modules
from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from PyQt5.QtWidgets import QMainWindow, QFileDialog

# UI Classes
from ui.main_window import Ui_MainWindow

# NetCDF packages
import netCDF4
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# MetPy packages
import metpy.calc as mpcalc
from metpy.testing import get_test_data
from metpy.units import units


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

    def button_clicked(self):
        self.test_push_button.setText(
            "Button Clicked")
        print("Button clicked")

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;NetCDF Files (*.nc)", options=options)
        if fileName:
            print(fileName)
            self.read_file(fileName)

    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "",
            "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            self.read_file(fileName)

    def read_file(self, fileName):
        """ Display the general information about the dataset and list all the 
        variables
        """
        ds = xr.open_dataset(fileName, decode_times=False)
        print(ds)

    # def scatter_plot(self, ds):
    #     fig = plt.figure()
    #     ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    #     ax.stock_img()
    #     ax.coastlines()
    #     sc = plt.scatter(ds['lon'].values, ds['lat'].values,
    #                     c=ds['observation'].values)
    #     plt.colorbar(sc)
    #     plt.show()


if __name__ == '__main__':
    APPCTXT = AppContext()
    EXIT_CODE = APPCTXT.run()
    sys.exit(EXIT_CODE)
