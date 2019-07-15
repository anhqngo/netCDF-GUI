"""Main source file for DART Viewer application
"""

# Standard library imports
import sys
import os
import numpy as np

# NetCDF library imports
import xarray as xr
from netCDF4 import Dataset

# PyQt5 library imports
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from fbs_runtime.application_context.PyQt5 import (
    ApplicationContext, cached_property)

# Local imports
from ui.main_window import Ui_MainWindow
from ui.subset_dialog import Ui_subset_dialog
from utils.io import walktree
from utils.plot import geo_3d_plot, time_series_qc_plot, qc_observations_plot


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
        self.setup_validators()
        self.open_file_dialog()

    def setup_slots(self):
        """This function connects pre-existing signals with the correct slots
        """
        self.actionOpen.triggered.connect(self.open_file_dialog)
        self.obsIndexPush.clicked.connect(self.show_parent_groups)
        self.plotButton.clicked.connect(self.master_plot)

    def setup_validators(self):
        """This function adds value validator for user input field. Users cannot
        input unspecified values.

        For example, the Regex "[0-9]+" specifies a positive integer.
        The field will not let users input any other values.
        """
        self.obsIndexInput.setValidator(
            QRegExpValidator(
                QRegExp("[0-9]+"),
                self.obsIndexInput))

    def open_file_dialog(self):
        """Open a dialog for user to chose their dataset
        """
        try:
            if os.environ['DEBUG'] == "true":
                dataset_path = os.environ['TEST_FILE']
        except KeyError:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            dataset_path, _ = QFileDialog.getOpenFileName(
                self, "Open NetCDF File", "",
                "NetCDF Files (*.nc);;All Files (*)", options=options)
        try:
            self.debugContents.append("Open file: {}".format(dataset_path))
            self.dataset = xr.open_dataset(dataset_path, decode_times=True)
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
        self.variableList.clear()
        self.variableList.addItems(list(self.dataset.data_vars))
        for children in walktree(self.root_group):
            for child in children:
                self.ds_group_list.append(child.name)
        self.groupContents.clear()
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
            self.parentGroupList.append("Input must be an integer")

    def get_selected_var(self):
        """Get variable selection from user input

        :return: variable name
        :rtype: string
        """
        return self.variableList.currentItem().text()

    def get_selected_group(self):
        """Get group selection from user input

        :return: group name
        :rtype: string
        """
        return self.groupContents.currentItem().text()

    def setup_subset_dialog_ui(self):
        """This function pre-fills the min and max values for time, lat and lon
        input fields
        """
        time = self.dataset['time'].values
        time_max = max(time)
        time_min = min(time)
        self.subset_dialog.time_max_input.setText(
            np.datetime_as_string(time_max, unit='s'))
        self.subset_dialog.time_min_input.setText(
            np.datetime_as_string(time_min, unit='s'))

        self.subset_dialog.lon_max_input.setText(
            str(np.around(max(self.dataset['lon'].values), decimals=2)))
        self.subset_dialog.lon_min_input.setText(
            str(np.around(min(self.dataset['lon'].values), decimals=2)))

        self.subset_dialog.lat_max_input.setText(
            str(np.around(max(self.dataset['lat'].values), decimals=2)))
        self.subset_dialog.lat_min_input.setText(
            str(np.around(min(self.dataset['lat'].values), decimals=2)))

    def get_dataset_subset(self):
        """Displays the subset dialog, takes user input, and returns the new
        dataset subset

        :param dataset: the original dataset
        :type dataset: xr.Dataset
        :return: the new dataset after subsetting
        :rtype: xr.Dataset
        """
        self.setup_subset_dialog_ui()
        self.subset_dialog.exec_()

        def subset_group(dataset):
            """[summary]

            :param dataset: [description]
            :type dataset: [type]
            :return: [description]
            :rtype: [type]
            """
            if self.get_selected_group() == "root":
                return dataset
            obs_index_array = self.root_group['/{}/obs_id'.format(
                self.get_selected_group())][:].compressed()
            new_dataset = dataset.loc[dict(obs=obs_index_array)]
            return new_dataset

        def subset_location(dataset):
            """Return a new dataset subset based on user's input on location
            """
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

            dataset = dataset.where(
                lat_max >= dataset.coords['lat'], drop=True)
            dataset = dataset.where(
                lat_min <= dataset.coords['lat'], drop=True)
            dataset = dataset.where(
                lon_max >= dataset.coords['lon'], drop=True)
            dataset = dataset.where(
                lon_min <= dataset.coords['lon'], drop=True)

            return dataset

        def subset_time(dataset):
            """Return a new dataset subset based on user's input on time
            """
            (time_max_input,
             time_min_input) = (self.subset_dialog.time_max_input.text(),
                                self.subset_dialog.time_min_input.text())
            if time_max_input:
                time_max_input = np.datetime64(time_max_input)
                dataset = dataset.where(
                    time_max_input >= dataset['time'], drop=True)
            if time_min_input:
                time_min_input = np.datetime64(time_min_input)
                dataset = dataset.where(
                    time_min_input <= dataset['time'], drop=True)
            return dataset

        def subset_qc(dataset):
            """Return a new dataset subset based on user's input on qc values
            """
            list_of_unchecked_checkboxes = []
            list_of_checkboxes = [self.subset_dialog.qc_checkbox_0,
                                  self.subset_dialog.qc_checkbox_1,
                                  self.subset_dialog.qc_checkbox_2,
                                  self.subset_dialog.qc_checkbox_3,
                                  self.subset_dialog.qc_checkbox_4,
                                  self.subset_dialog.qc_checkbox_5,
                                  self.subset_dialog.qc_checkbox_6,
                                  self.subset_dialog.qc_checkbox_7,
                                  self.subset_dialog.qc_checkbox_8]
            for box in list_of_checkboxes:
                if not box.isChecked():
                    list_of_unchecked_checkboxes.append(
                        list_of_checkboxes.index(box))
            # If none of the boxes is checked, then treat it like box "All" is
            # checked
            if (len(list_of_unchecked_checkboxes) == 9) or (
                    8 not in list_of_unchecked_checkboxes):
                return dataset

            for i in list_of_unchecked_checkboxes:
                dataset = dataset.where(i != dataset['qc'], drop=True)
            try:
                dataset = dataset.squeeze('qc_copy')
            except BaseException:
                # TODO: fix me
                print("Im not sure what to do")
            return dataset

        return subset_time(
            subset_qc(
                subset_location(
                    subset_group(
                        self.dataset))))

    def master_plot(self):
        """Generate all the necessary plots for a single netCDF file
        """
        dataset = self.get_dataset_subset()
        variable = self.get_selected_var()

        if dataset['obs'].values.size:
            geo_3d_plot(dataset, variable)
            time_series_qc_plot(dataset)
            qc_observations_plot(dataset)
        else:
            self.debugContents.append(
                "No observation values satisfy user input range")


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
