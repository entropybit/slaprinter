# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SlicingWindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(796, 638)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 11, 781, 501))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.OpenGlPanel = QtGui.QHBoxLayout(self.layoutWidget)
        self.OpenGlPanel.setMargin(0)
        self.OpenGlPanel.setObjectName(_fromUtf8("OpenGlPanel"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.OpenGlPanel.addItem(spacerItem)
        self.algorithmLabel = QtGui.QLabel(self.centralwidget)
        self.algorithmLabel.setGeometry(QtCore.QRect(20, 525, 761, 41))
        self.algorithmLabel.setObjectName(_fromUtf8("algorithmLabel"))
        self.prevButton = QtGui.QPushButton(self.centralwidget)
        self.prevButton.setGeometry(QtCore.QRect(20, 560, 79, 25))
        self.prevButton.setObjectName(_fromUtf8("prevButton"))
        self.nextButton = QtGui.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(110, 560, 79, 25))
        self.nextButton.setObjectName(_fromUtf8("nextButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 796, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.algorithmLabel.setText(_translate("MainWindow", "Algorithm Output", None))
        self.prevButton.setText(_translate("MainWindow", "Prev", None))
        self.nextButton.setText(_translate("MainWindow", "Next", None))

