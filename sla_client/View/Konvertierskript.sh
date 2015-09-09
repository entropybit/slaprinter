#!/bin/bash

pyuic4 StandardWindow.ui > StandardWindow.py
pyuic4 PrinterSettings.ui > PrinterSettings.py
pyuic4 PrintingWindow.ui > PrintingWindow.py
pyuic4 PrintingDialog.ui > PrintingDialog.py
#pyuic4 SlicingDialog.ui > SlicingDialog.py
pyuic4 SlicingWindow.ui > SlicingWindow.py
