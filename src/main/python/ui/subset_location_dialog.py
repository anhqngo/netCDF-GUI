# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/main/resources/designer/subset_location_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_subset_location_dialog(object):
    def setupUi(self, subset_location_dialog):
        subset_location_dialog.setObjectName("subset_location_dialog")
        subset_location_dialog.resize(325, 201)
        self.widget = QtWidgets.QWidget(subset_location_dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 304, 173))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lon_min_label = QtWidgets.QLabel(self.frame)
        self.lon_min_label.setObjectName("lon_min_label")
        self.verticalLayout.addWidget(self.lon_min_label)
        self.lon_min_input = QtWidgets.QLineEdit(self.frame)
        self.lon_min_input.setText("")
        self.lon_min_input.setObjectName("lon_min_input")
        self.verticalLayout.addWidget(self.lon_min_input)
        self.lat_min_label = QtWidgets.QLabel(self.frame)
        self.lat_min_label.setObjectName("lat_min_label")
        self.verticalLayout.addWidget(self.lat_min_label)
        self.lat_min_input = QtWidgets.QLineEdit(self.frame)
        self.lat_min_input.setObjectName("lat_min_input")
        self.verticalLayout.addWidget(self.lat_min_input)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lon_max_label = QtWidgets.QLabel(self.frame)
        self.lon_max_label.setObjectName("lon_max_label")
        self.verticalLayout_2.addWidget(self.lon_max_label)
        self.lon_max_input = QtWidgets.QLineEdit(self.frame)
        self.lon_max_input.setObjectName("lon_max_input")
        self.verticalLayout_2.addWidget(self.lon_max_input)
        self.lat_max_label = QtWidgets.QLabel(self.frame)
        self.lat_max_label.setObjectName("lat_max_label")
        self.verticalLayout_2.addWidget(self.lat_max_label)
        self.lat_max_input = QtWidgets.QLineEdit(self.frame)
        self.lat_max_input.setObjectName("lat_max_input")
        self.verticalLayout_2.addWidget(self.lat_max_input)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.lon_min_input.raise_()
        self.lat_min_input.raise_()
        self.lon_max_input.raise_()
        self.lat_max_input.raise_()
        self.lon_min_label.raise_()
        self.lat_min_label.raise_()
        self.lat_max_label.raise_()
        self.lon_max_label.raise_()
        self.lon_max_input.raise_()
        self.verticalLayout_3.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(subset_location_dialog)
        self.buttonBox.accepted.connect(subset_location_dialog.accept)
        self.buttonBox.rejected.connect(subset_location_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(subset_location_dialog)

    def retranslateUi(self, subset_location_dialog):
        _translate = QtCore.QCoreApplication.translate
        subset_location_dialog.setWindowTitle(_translate("subset_location_dialog", "Dialog"))
        self.lon_min_label.setText(_translate("subset_location_dialog", "Lon min"))
        self.lat_min_label.setText(_translate("subset_location_dialog", "Lat min"))
        self.lon_max_label.setText(_translate("subset_location_dialog", "Lon max"))
        self.lat_max_label.setText(_translate("subset_location_dialog", "Lat max"))

