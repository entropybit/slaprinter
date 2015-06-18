__author__ = 'aslan'

import json
import os.path

from PyQt4.QtGui import *





#from PyQt4.QtCore import pyqtSlot

from StandardWindow import Ui_MainWindow
from PrintingDialog import Ui_Dialog as Ui_PrintingDialog
from PrintingWindow import Ui_MainWindow as Ui_PrintingWindow
from PrinterSettings import Ui_Dialog as Ui_PrinterSettings

from QlWidget import *#GLWidget

app = QApplication(sys.argv)

#Initiating standard window
mainWindow = QMainWindow()
ui1 = Ui_MainWindow()
ui1.setupUi(mainWindow)
glMain  = GLWidget()
ui1.OpenGlPanel.addWidget(glMain)

#Initiating printer settings dialogue (individual options for each print)
printingDialog = QDialog()
ui2 = Ui_PrintingDialog()
ui2.setupUi(printingDialog)

#Initiating printing window
printingWindow = QMainWindow()
ui3 = Ui_PrintingWindow()
ui3.setupUi(printingWindow)
glStatus = GLWidget()
ui3.OpenGlPanel.addWidget(glStatus)

#Initiating general printer settings window (for overarching printer settings that are always the same with the same printer)
printerSettings = QDialog()
ui4 = Ui_PrinterSettings()
ui4.setupUi(printerSettings)


def switchToPrintingMode():
   mainWindow.close()
   printerSettings.close() #shouldnt be open at this point, but you never know
   printingDialog.close()
   printingWindow.show()



def savePrinterSettingsToFile():
   configfile = open('PrinterSettings.conf', 'w')
   SettingsList= ['AreaWidth=', float(ui4.AreaWidth.text()), 'AreaLength=', float(ui4.AreaLength.text()),'AreaHeight=', float(ui4.AreaHeight.text()),
        'HeightPerRevolution=', float(ui4.HeightPerRevolution.text()), 'StepsPerRevolution=', float(ui4.StepsPerRevolution.text()),
        'ipAdress=', str(ui4.ipAdress.text()), 'illuminationTime=', float(ui4.illuminationTime.text()),
        'illuminationIntensity=', float(ui4.illuminationIntensity.text()), 'PrinterLiquidPrice=', float(ui4.PrinterLiquidPrice.text())]
   json.dump(SettingsList, configfile)
   configfile.close()

   printerSettings.close() #closes the window


def loadPrinterSettings():

    configfile = open('PrinterSettings.conf', 'r')
    SettingsList=json.load(configfile)

    ui4.AreaWidth.clear()
    ui4.AreaWidth.insert('%d' % SettingsList[1])
    ui4.AreaLength.clear()
    ui4.AreaLength.insert('%d' % SettingsList[3])
    ui4.AreaHeight.clear()
    ui4.AreaHeight.insert('%d' % SettingsList[5])
    ui4.HeightPerRevolution.clear()
    ui4.HeightPerRevolution.insert('%d' % SettingsList[7])
    ui4.StepsPerRevolution.clear()
    ui4.StepsPerRevolution.insert('%d' % SettingsList[9])
    ui4.ipAdress.clear()
    ui4.ipAdress.insert(SettingsList[11])
    ui4.illuminationTime.clear()
    ui4.illuminationTime.insert('%d' % SettingsList[13])
    ui4.illuminationIntensity.clear()
    ui4.illuminationIntensity.insert('%d' % SettingsList[15])
    ui4.PrinterLiquidPrice.clear()
    ui4.PrinterLiquidPrice.insert('%d' % SettingsList[17])

    configfile.close()



def MoveStepper(up=True, no_of_steps=1): #This is going to be the motor step function
   print up
   print no_of_steps

def MoveStepperToEndPos(Endposition=True):
   #False is Startposition
   pass


def ManualPrintingAbort():
   w = QWidget()
   QMessageBox.critical(w, 'Message', 'Printing stopped by user!')
   MoveStepperToEndPos(True)
   printingWindow.close()
   mainWindow.show()

def fileDialogFunction():
    filename = QFileDialog.getOpenFileName(mainWindow, 'Open File') #LINUX
#    filename = QFileDialog.getOpenFileName(mainWindow, 'Open File', 'C:\') #WINDOWS
    print filename
# print file contents
    with open(filename, 'r') as f:
        print(f.read())
    file.close()


#Explaining what each button on the StandardWindow does
ui1.importFileButton.clicked.connect(fileDialogFunction)
ui1.StartPrintButton.clicked.connect(printingDialog.show)
ui1.printerSettingsButton.clicked.connect(printerSettings.show)
#ui1.DownPosButton.clicked.connect(MoveStepper, [False,2])            #why cant i call functions with parameters?
#ui1.UpPosButton.clicked.connect(MoveStepper(True, N))


"""
#Das hier sind die Zeilen die editLine-objekten ihre Werte ein bzw ausgibt.
fisch= int(ui1.N.text())
N=6
ui1.N.clear()
ui1.N.insert('%d' % N)
print fisch
print fisch.__class__
"""

#Explaining what each button on the PrintingDialog does
ui2.OkButton.clicked.connect(switchToPrintingMode)
ui2.CancelButton.clicked.connect(printingDialog.close)

#Explaining what each button on the PrintingWindow does
ui3.StopPrintButton.clicked.connect(ManualPrintingAbort)

#Explaining what each button on the  printingSettingsWindow does
if os.path.isfile('PrinterSettings.conf'):
    loadPrinterSettings()
ui4.CancelButton.clicked.connect(printerSettings.close)
ui4.OkButton.clicked.connect(savePrinterSettingsToFile)





