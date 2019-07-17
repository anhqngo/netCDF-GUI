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
from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QDialog,
    QCheckBox,
    QErrorMessage,
    QMessageBox)
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from fbs_runtime.application_context.PyQt5 import (
    ApplicationContext, cached_property)

# Local imports
from ui.main_window import Ui_MainWindow
from ui.subset_dialog import Ui_subset_dialog
from utils.io import walktree
from utils.plot import geo_3d_plot, time_series_qc_plot, qc_observations_plot
from functools import reduce


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

    def show_error_messages(self, error_message):
        """This function display an error message dialog to the user

        :param error_message: Name of the error that the user is encountering
        :type error_message: string
        """
        error_dialog = QErrorMessage()
        error_dialog.setWindowTitle("Error")
        error_dialog.showMessage(error_message)
        error_dialog.exec_()

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
            self.ds_group_list = ['root']
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
        for children in walktree(self.root_group):
            for child in children:
                self.ds_group_list.append(child.name)

        # A dictionary that maps group_name (string) to QCheckbox type
        self.groupDict = dict()
        for group in self.ds_group_list:
            self.groupDict[group] = QCheckBox(self.groupListFrame)
            self.verticalLayout.addWidget(self.groupDict[group])
            self.groupDict[group].setObjectName('{}_checkbox'.format(group))
            self.groupDict[group].setText(group)

    def show_parent_groups(self):
        """Display all the groups that an observation is in based on user's
        input of observation index
        """
        obs_index = int(self.obsIndexInput.text())
        # Only take valid indices from the array:
        groups = np.where(
            self.dataset['list_of_groups'].values[obs_index] >= 0)[0]

        self.parentGroupList.clear()    # reset the text browser
        if groups.size:
            for group in groups:
                # +1 because the first item is rootgroup
                self.parentGroupList.addItem(self.ds_group_list[group + 1])
        else:
            self.parentGroupList.addItem("No groups available")

    def get_selected_var(self):
        """Get variable selection from user input

        :return: variable name
        :rtype: string
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
        :rtype: Python list with type string
        """
        list_of_checked = []
        for checkbox_string in self.groupDict:
            checkbox = self.groupDict[checkbox_string]
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
            checked_group_list = self.get_selected_groups()
            if len(checked_group_list) == 0:
                return dataset

            def get_obs_id_list(checked_group_list):
                """[summary]

                :param checked_group_list: [description]
                :type checked_group_list: [type]
                :return: [description]
                :rtype: [type]
                """
                obs_id_list = []
                for group in checked_group_list:
                    obs_id = self.root_group['/{}/obs_id'.format(
                        group)][:].compressed()
                    obs_id_list.append(obs_id)
                return obs_id_list

            if self.and_radioButton.isChecked():
                if len(checked_group_list) < 2:
                    self.show_error_messages("Please select at least 2 groups")
                    return
                if "root" in checked_group_list:
                    checked_group_list.remove("root")
                from functools import reduce
                print(checked_group_list)
                print(get_obs_id_list(checked_group_list))
                obs_index_array = reduce(
                    np.intersect1d, get_obs_id_list(checked_group_list))
            else:
                if "root" in checked_group_list:
                    return dataset
                obs_index_array = np.unique(np.concatenate(
                    get_obs_id_list(checked_group_list)))

            dataset = dataset.loc[dict(obs=obs_index_array)]
            return dataset

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
            list_of_unchecked = []
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
                    list_of_unchecked.append(
                        list_of_checkboxes.index(box))
            # If none of the boxes is checked, then treat it like box "All" is
            # checked
            if (len(list_of_unchecked) == 9) or (
                    8 not in list_of_unchecked):
                return dataset

            for i in list_of_unchecked:
                dataset = dataset.where(i != dataset['qc'], drop=True)
            try:
                dataset = dataset.squeeze('qc_copy')
            except BaseException:
                # TODO: The varible qc has qc_copy x obs dinension. Therefore,
                # when we use dataset.where with qc variable, the qc_copy
                # dimension gets pushed to all other variables (play around
                # with Jupyter Notebook to see this). Therefore, I have to
                # squeeze the dataset (i.e. remove that dimension). If the
                # squeezing fails for some reason (potentially because there
                # are more than one qc_copy values), then I honestly do not
                # know what to do.
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
