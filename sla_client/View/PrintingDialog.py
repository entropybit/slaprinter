# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PrintingDialog.ui'
#
# Created: Wed Sep  9 23:12:28 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(347, 261)
        self.horizontalLayout_6 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.sliceThickness = QtGui.QLineEdit(Dialog)
        self.sliceThickness.setObjectName(_fromUtf8("sliceThickness"))
        self.horizontalLayout.addWidget(self.sliceThickness)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.checkBoxFloat = QtGui.QCheckBox(Dialog)
        self.checkBoxFloat.setObjectName(_fromUtf8("checkBoxFloat"))
        self.horizontalLayout_2.addWidget(self.checkBoxFloat)
        self.checkBoxSupports = QtGui.QCheckBox(Dialog)
        self.checkBoxSupports.setObjectName(_fromUtf8("checkBoxSupports"))
        self.horizontalLayout_2.addWidget(self.checkBoxSupports)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.radioButtonGorilla = QtGui.QRadioButton(self.groupBox)
        self.radioButtonGorilla.setEnabled(True)
        self.radioButtonGorilla.setGeometry(QtCore.QRect(0, 20, 102, 22))
        self.radioButtonGorilla.setObjectName(_fromUtf8("radioButtonGorilla"))
        self.radioButtonTeflon = QtGui.QRadioButton(self.groupBox)
        self.radioButtonTeflon.setGeometry(QtCore.QRect(0, 40, 102, 22))
        self.radioButtonTeflon.setObjectName(_fromUtf8("radioButtonTeflon"))
        self.horizontalLayout_3.addWidget(self.groupBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_3.addWidget(self.label_5)
        self.fillPercentage = QtGui.QLineEdit(Dialog)
        self.fillPercentage.setObjectName(_fromUtf8("fillPercentage"))
        self.horizontalLayout_3.addWidget(self.fillPercentage)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName(_fromUtf8("CancelButton"))
        self.horizontalLayout_5.addWidget(self.CancelButton)
        self.OkButton = QtGui.QPushButton(Dialog)
        self.OkButton.setObjectName(_fromUtf8("OkButton"))
        self.horizontalLayout_5.addWidget(self.OkButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_3.setText(_translate("Dialog", "Slice Thickness (mm):", None))
        self.sliceThickness.setText(_translate("Dialog", "1", None))
        self.checkBoxFloat.setText(_translate("Dialog", "Enable Float?", None))
        self.checkBoxSupports.setText(_translate("Dialog", "Enable Supports?", None))
        self.groupBox.setTitle(_translate("Dialog", "Printing Mode", None))
        self.radioButtonGorilla.setText(_translate("Dialog", "GorillaGlass", None))
        self.radioButtonTeflon.setText(_translate("Dialog", "Teflon", None))
        self.label_5.setText(_translate("Dialog", "Fill  ", None))
        self.fillPercentage.setText(_translate("Dialog", "50", None))
        self.label_6.setText(_translate("Dialog", "%", None))
        self.CancelButton.setText(_translate("Dialog", "Cancel", None))
        self.OkButton.setText(_translate("Dialog", "Ok", None))

