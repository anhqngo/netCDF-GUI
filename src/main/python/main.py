"""Main source file for DART Viewer application
"""

# Standard library imports
import sys
import os
import re
from functools import reduce
import numpy as np

# NetCDF library imports
import xarray as xr
from netCDF4 import Dataset

# PyQt5 library imports
from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QDialog,
    QCheckBox,
    QErrorMessage)
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

    :param: ApplicationContext
    :type: fbs_runtime.application_context.PyQt5.ApplicationContext()

    """

    def run(self):
        self.main_window.show()
        return self.app.exec_()

    @cached_property
    def main_window(self):
        """This method renders the main window and makes it an attribute of
        the application context using the `@cached_property`
        """
        main_window = MainWindow(self)
        main_window.setWindowTitle(
            self.build_settings['app_name'] + " v." +
            self.build_settings['version'])
        return main_window


class MainWindow(QMainWindow, Ui_MainWindow):
    """This class that renders the main window for the GUI

    :param QMainWindow: Default class for main window in PyQt5
    :type QMainWindow: PyQt5.Widgets.QMainWindow
    :param Ui_MainWindow: This class is generated from the designer file (.ui)
    :type Ui_MainWindow: UI_MainWindow
    :return: None
    :rtype: None
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

        For example, one of the fields uses Regex "[0-9]+" as its validator
        This field will not let users input any non-integer values.
        """
        self.obsIndexInput.setValidator(
            QRegExpValidator(
                QRegExp("[0-9]+"),
                self.obsIndexInput))

    def show_error_messages(self, error_message):
        """This function display an error message dialog to the user

        :param error_message: Name of the error that the user is encountering
        :type error_message: str
        """
        error_dialog = QErrorMessage()
        error_dialog.setWindowTitle("Error")
        error_dialog.showMessage(error_message)
        error_dialog.exec_()

    def open_file_dialog(self):
        """Open a dialog for user to chose their dataset
        """
        try:
            if os.environ['DEVELOPMENT'] == "true":
                dataset_path = os.environ['TEST_FILE']
        except KeyError:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            dataset_path, _ = QFileDialog.getOpenFileName(
                self, "Open NetCDF File", "",
                "NetCDF Files (*.nc);;All Files (*)", options=options)
        try:
            self.dataset = xr.open_dataset(dataset_path, decode_times=True)
            self.root_group = Dataset(dataset_path, "r", format="NETCDF4")
            self.ds_group_list = ['root']
            # A dictionary that maps group_name (str()) to QCheckbox type
            self.group_dict = dict()
            self.show_dataset_info()
        except OSError:
            error_message = "Invalid. Please choose a different file"
            self.show_error_messages(error_message)

    def show_dataset_info(self):
        """
        Display the general information about the dataset and list all the
        variables on the GUI
        """
        self.headerContents.setText(str(self.dataset))
        self.variableList.clear()
        self.variableList.addItems(list(self.dataset.data_vars))
        ds_group_list_temp = []
        for children in walktree(self.root_group):
            for child in children:
                ds_group_list_temp.append(child.path)
        self.ds_group_list += sorted(ds_group_list_temp)

        for group in self.ds_group_list:
            self.group_dict[group] = QCheckBox(self.groupListFrame)
            self.verticalLayout.addWidget(self.group_dict[group])
            self.group_dict[group].setObjectName('{}_checkbox'.format(group))
            self.group_dict[group].setText(group)

    def show_parent_groups(self):
        """Display all the groups that an observation is in based on user's
        input of observation index
        """

        obs_index = int(self.obsIndexInput.text())
        self.parentGroupList.clear()

        for group in self.ds_group_list:
            try:
                obs_id = self.root_group['{}/obs_id'.format(
                    group)][:].compressed()
                if obs_index == obs_id[np.searchsorted(obs_id, obs_index)]:
                    self.parentGroupList.addItem(group)
            except BaseException:
                continue

        if self.parentGroupList.count() == 0:
            self.parentGroupList.addItem("No groups available")

    def get_selected_var(self):
        """Get variable selection from user input

        :return: variable name
        :rtype: str()
        """
        selected_var = self.variableList.currentItem().text()
        if selected_var:
            return selected_var
        else:
            self.show_error_messages(
                "Please choose a variable from the list to plot")

    def get_selected_groups(self):
        """Get group selection from user input

        :return: list of group names
        :rtype: Python list with type str()
        """
        list_of_checked = []
        for checkbox_string in self.group_dict:
            checkbox = self.group_dict[checkbox_string]
            if checkbox.isChecked():
                list_of_checked.append(checkbox_string)
        return list_of_checked

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
        dataset subset.

        The function is broken down into four helper functions, which helps
        subset the dataset based on groups, location, time, and QC Values.

        :param dataset: the original dataset
        :type dataset: xr.Dataset()
        :return: the new dataset after subsetting
        :rtype: xr.Dataset()
        """
        self.setup_subset_dialog_ui()
        self.subset_dialog.exec_()

        def subset_group(dataset):
            checked_group_list = self.get_selected_groups()
            if not checked_group_list:
                return dataset

            def get_obs_id_list(checked_group_list):
                """Given a list of checked groups, this function returns a list
                of obs_id arrays in those groups.

                :param checked_group_list: List of groups that user selected
                :type checked_group_list: List of strings
                :return: A list of obs_id arrays in those groups
                :rtype: List of lists
                """
                obs_id_list = []
                for group in checked_group_list:
                    if self.root_group['{}'.format(group)].groups:
                        new_list = [
                            x for x in self.ds_group_list if re.search(
                                r'^{}/+'.format(group), x)]
                        checked_group_list.remove(group)
                        checked_group_list += new_list
                for group in checked_group_list:
                    obs_id = self.root_group['{}/obs_id'.format(
                        group)][:].compressed()
                    obs_id_list.append(obs_id)

                return obs_id_list

            if self.and_radioButton.isChecked():
                if len(checked_group_list) < 2:
                    self.show_error_messages("Please select at least 2 groups")
                    return
                if "root" in checked_group_list:
                    checked_group_list.remove("root")
                obs_index_array = reduce(
                    np.intersect1d, get_obs_id_list(checked_group_list))
            else:
                if "root" in checked_group_list:
                    return dataset
                obs_index_array = np.unique(np.concatenate(
                    get_obs_id_list(checked_group_list)))

            dataset = dataset.loc[dict(obs=obs_index_array)]
            if dataset['obs'].values.size:
                return dataset
            else:
                self.show_error_messages(
                    "No observation values satisfy user input range")

        def subset_location(dataset):
            # TODO: change the code below to check whether the default lon/lat
            # values has been changed or not to avoid unnecessary computations

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

            if dataset['obs'].values.size:
                return dataset
            else:
                self.show_error_messages(
                    "No observation values satisfy user input range")

        def subset_time(dataset):
            # TODO: change the code below to check whether the default text has
            # been changed or not to avoid unnecessary computations
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

            if dataset['obs'].values.size:
                return dataset
            else:
                self.show_error_messages(
                    "No observation values satisfy user input range")
            return dataset

        def subset_qc(dataset):
            list_of_checked = []
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
                if box.isChecked():
                    list_of_checked.append(
                        list_of_checkboxes.index(box))

            # If none of the boxes is checked, then treat it like box "All" is
            # checked
            if (not list_of_checked) or (8 in list_of_checked):
                return dataset

            obs_index_array = np.concatenate([np.where(dataset['qc'].T[1].values == i)[
                0] for i in list_of_checked], axis=0)

            dataset = dataset.loc[dict(obs=obs_index_array)]
            if dataset['obs'].values.size:
                return dataset
            else:
                self.show_error_messages(
                    "No observation values satisfy user input range")

        return subset_time(
            subset_qc(
                subset_location(
                    subset_group(
                        self.dataset))))

    def master_plot(self):
        """Generate all the necessary plots for a single netCDF file

        The plots generated are:
        - Geo 3D Plot
        - Time series of quality control values
        - Counts of observations based on QC Values
        """
        dataset = self.get_dataset_subset()
        variable = self.get_selected_var()

        if dataset['obs'].values.size:
            try:
                geo_3d_plot(dataset, variable)
            except BaseException:
                error_message = "Unable to produce plots Geo 3D Plot.\n\
                    Perhaps the variable that you chose is not compatible"
                self.show_error_messages(error_message)
            time_series_qc_plot(dataset)
            qc_observations_plot(dataset)
        else:
            self.show_error_messages(
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
