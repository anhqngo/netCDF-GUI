"""Main source file for DART Viewer application
"""

# Standard library imports
import sys
import numpy as np

# NetCDF library imports
import xarray as xr
from netCDF4 import Dataset

# PyQt5 library imports
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property

# Local imports
from ui.main_window import Ui_MainWindow
from utils.io import walktree


class AppContext(ApplicationContext):
    """This class sets up Application context for fman build

    :param ApplicationContext: built-in class from fbs_runtime.application_context.PyQt5
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
            "DART Plotting Tool v." +
            self.build_settings['version'])
        return main_window


class MainWindow(QMainWindow, Ui_MainWindow):
    """This is the main class that renders the main GUI
    """

    def __init__(self, ctx):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.ctx = ctx
        self.setup_slots()
        self.open_file_dialog()

    def setup_slots(self):
        """This function connects pre-existing signals with the correct slots
        """
        self.actionOpen.triggered.connect(self.open_file_dialog)
        # self.variableList.itemDoubleClicked.connect(self.show_variable)
        # self.groupContents.itemDoubleClicked.connect(
        #     self.plot_obseravtions_in_group)
        self.obsIndexPush.clicked.connect(self.show_parent_groups)

    def open_file_dialog(self):
        """Open a dialog for user to chose their dataset
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dataset_path, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;NetCDF Files (*.nc)", options=options)
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


if __name__ == '__main__':
    APPCTXT = AppContext()
    EXIT_CODE = APPCTXT.run()
    sys.exit(EXIT_CODE)
