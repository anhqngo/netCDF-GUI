"""Main source file for DART Viewer application
"""

# Standard library imports
import sys
import numpy as np

# NetCDF library imports
import xarray as xr
from netCDF4 import Dataset

# PyQt5 library imports
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog
from fbs_runtime.application_context.PyQt5 import (
    ApplicationContext, cached_property)

# Local imports
from ui.main_window import Ui_MainWindow
from ui.subset_dialog import Ui_subset_dialog
from utils.io import walktree
from utils.plot import geo_3d_plot


class AppContext(ApplicationContext):
    """This class sets up Application context for fman build
    """

    def run(self):
        self.main_window.show()
        return self.app.exec_()

    @cached_property
    def main_window(self):
        """Property method to render the main window
        """
        main_window = MainWindow(self)
        main_window.setWindowTitle(
            self.build_settings['app_name'] +
            self.build_settings['version'])
        return main_window


class MainWindow(QMainWindow, Ui_MainWindow):
    """This is the main class that renders the main GUI
    """

    def __init__(self, ctx):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.ctx = ctx
        self.subset_dialog = SubsetDialog()
        self.setup_slots()
        self.open_file_dialog()

    def setup_slots(self):
        """This function connects pre-existing signals with the correct slots
        """
        self.actionOpen.triggered.connect(self.open_file_dialog)
        self.plotButton.clicked.connect(
            lambda: geo_3d_plot(
                self.dataset_subset,
                "observations",
                np.arange(2323)))
        self.obsIndexPush.clicked.connect(self.show_parent_groups)

    def open_file_dialog(self):
        """Open a dialog for user to chose their dataset
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dataset_path, _ = QFileDialog.getOpenFileName(
            self, "Open NetCDF File", "",
            "NetCDF Files (*.nc);;All Files (*)", options=options)
        try:
            self.debugContents.append("Open file: {}".format(dataset_path))
            self.dataset = xr.open_dataset(dataset_path, decode_times=False)
            self.root_group = Dataset(dataset_path, "r", format="NETCDF4")
            self.ds_group_list = []
            self.show_dataset_info()
        except OSError:
            self.debugContents.append(
                "Invalid. Please choose a different file")

    def show_dataset_info(self):
        """
        Display the general information about the dataset and list all the
        variables on the GUI
        """
        self.headerContents.setText(str(self.dataset))
        self.variableList.addItems(list(self.dataset.data_vars))
        for children in walktree(self.root_group):
            for child in children:
                self.ds_group_list.append(child.name)
        self.groupContents.addItem("root")
        self.groupContents.addItems(self.ds_group_list)

    def show_parent_groups(self):
        """Display all the groups that an observation is in based on user's
        input of observation index
        """
        try:
            obs_index = int(self.obsIndexInput.text())
            # Only take valid indices from the array:
            groups = np.where(
                self.dataset['list_of_groups'].values[obs_index] >= 0)[0]
            # Reset the textbrowser and get ready to display groups:
            self.parentGroupList.setText("")
            if groups.size:
                for group in groups:
                    self.parentGroupList.append(self.ds_group_list[group])
            else:
                self.parentGroupList.setText("No groups available")
        except ValueError:
            self.parentGroupList.append("Must be an integer")

    @cached_property
    def dataset_subset(self):
        """Displays the subset dialog, takes user input, and returns the new
        dataset

        :param dataset: the original dataset
        :type dataset: xr.Dataset
        :return: the new dataset after subsetting
        :rtype: xr.Dataset
        """
        self.subset_dialog.exec_()

        (lon_max_input,
         lat_max_input,
         lon_min_input,
         lat_min_input) = (self.subset_dialog.lon_max_input.text(),
                           self.subset_dialog.lat_max_input.text(),
                           self.subset_dialog.lon_min_input.text(),
                           self.subset_dialog.lat_min_input.text())
        lon_max = float(lon_max_input) if lon_max_input else np.Inf
        lon_min = float(lon_min_input) if lon_min_input else -np.Inf
        lat_max = float(lat_max_input) if lat_max_input else np.Inf
        lat_min = float(lat_min_input) if lat_min_input else -np.Inf

        ds_temp = self.dataset.where(
            lat_max >= self.dataset.coords['lat'].astype('float'))
        ds_temp = ds_temp.where(
            lat_min <= ds_temp.coords['lat'], drop=True)
        ds_temp = ds_temp.where(
            lon_max >= ds_temp.coords['lon'], drop=True)
        ds_temp = ds_temp.where(
            lon_min <= ds_temp.coords['lon'], drop=True)
        return ds_temp

    def get_obs_index_array(self):
        """Given a group from user input, this function returns the list of
        observation indices in that group

        :param selected_group: user selected group from a list of groups
        :type selected_group: string
        :return: list of observation indices in that group
        :rtype: np.array
        """
        selected_group = self.groupContents.itemClicked().text()
        if selected_group == "root":
            return self.dataset['obs'].values
        else:
            return self.root_group['/{}/obs_id'.format(
                selected_group)][:].compressed()


class SubsetDialog(QDialog, Ui_subset_dialog):
    """This class displays the UI for SubsetDialog
    """

    def __init__(self):
        super(SubsetDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Subset Dialog")


if __name__ == '__main__':
    APPCTXT = AppContext()
    EXIT_CODE = APPCTXT.run()
    sys.exit(EXIT_CODE)
