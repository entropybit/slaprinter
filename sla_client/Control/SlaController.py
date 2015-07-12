__author__ = 'mithrawnuruodo'

from PyQt4.QtGui import QApplication, QMainWindow, QDialog, QWidget, QMessageBox, QFileDialog
from PyQt4 import QtCore
from View import Ui_MainWindow, GLWidget, Ui_PrinterSettings, Ui_PrintingDialog, Ui_PrintingWindow, StlModelView
from View import Ui_SlicingWindow
from Model import StlModel
import json, requests, time
import sys
import os.path
PROJECT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]



class SlaController(QApplication):

    def __init__(self, argv):
        QApplication.__init__(self, argv)

        # main window
        self.__mainWindow = QMainWindow()
        self.__ui1 = Ui_MainWindow()
        self.__glMain = object()
        self.__stl_model = StlModel()
        self.__stl_view = None

        # printing dialog
        self.__printingDialog = QDialog()
        self.__ui2 = Ui_PrintingDialog()

        # printing window
        self.__printingWindow = QMainWindow()
        self.__ui3 = Ui_PrintingWindow()
        self.__glStatus = object()

        # printer settings
        self.__printerSettings = QDialog()
        self.__ui4 = Ui_PrinterSettings()

        # slicing dialog
        # ToDo find something working as DropDown or get ComboBox working
        #self.__ui5 = ...

        # slicing window
        self.__glSlice = object()
        self.__slicingwindow = QMainWindow()
        self.__ui6 = Ui_SlicingWindow()

    def start(self):
        self.initWindows()
        self.makeConnections()
        self.__mainWindow.show()
        sys.exit(self.exec_())

    def initWindows(self):


        self.init_main()
        self.init_printer_settings()
        self.init_printing_window()
        self.init_printing_dialog()
        # self.init_slicing_dialog()
        self.init_slicing_window()



    def init_main(self):
        self.__glMain  = GLWidget()
        self.__ui1.setupUi(self.__mainWindow)
        self.__ui1.OpenGlPanel.addWidget(self.__glMain)
       # self.installEventFilter(self.__glMain)

    def init_printing_dialog(self):
        '''
            Initiating printer settings dialogue (individual options for each print)
        '''
        self.__ui2.setupUi(self.__printingDialog)

    def init_printer_settings(self):
        '''
            Initiating general printer settings window (for overarching printer settings that are always the same with the same printer)
        '''
        self.__ui4.setupUi(self.__printerSettings)

    def init_printing_window(self):
        '''
            Initiating printing window
        '''
        self.__glStatus = GLWidget()
        self.__ui3.setupUi(self.__printingWindow)
        self.__ui3.OpenGlPanel.addWidget(self.__glStatus)

    def init_slicing_window(self):
        '''
            Initializing slicing window
        '''
        self.__glSlice  = GLWidget()
        self.__glSlice.allow_rot = False
        self.__glSlice.allow_zoom = False

        self.__ui6.setupUi(self.__slicingwindow)
        self.__ui6.OpenGlPanel.addWidget(self.__glSlice)


    def makeConnections(self):
        '''
            make connections between signal and slots so that user interactions lead to according
            actions on the model or view
        '''
        self.__ui1.importFileButton.clicked.connect(self.fileDialogFunction)
        self.__ui1.StartPrintButton.clicked.connect(self.__printingDialog.show)
        self.__ui1.printerSettingsButton.clicked.connect(self.__printerSettings.show)
        self.__ui1.CenterButton.clicked.connect(self.__glMain.reset)
        self.__ui1.MeshButton.clicked.connect(self.__glMain.mesh)
        self.__ui1.BoundingBoxButton.clicked.connect(self.__glMain.bounding_box)
        self.__ui1.SlicingButton.clicked.connect(self.__slicingwindow.show)
        #ui1.DownPosButton.clicked.connect(MoveStepper, [False,2])            #why cant i call functions with parameters?
        #ui1.UpPosButton.clicked.connect(MoveStepper(True, N))

    def switchToPrintingMode(self):
        self.__mainWindow.close()
        self.__printerSettings.close() #shouldnt be open at this point, but you never know
        self.__printingDialog.close()
        self.__printingWindow.show()
        self.sendToRaspberry()

    def savePrinterSettingsToFile(self):
        configfile = open('PrinterSettings.conf', 'w')
        SettingsList= ['AreaWidth=', float(self.__ui4.AreaWidth.text()), 'AreaLength=', float(self.__ui4.AreaLength.text()),'AreaHeight=', float(self.__ui4.AreaHeight.text()),
            'HeightPerRevolution=', float(self.__ui4.HeightPerRevolution.text()), 'StepsPerRevolution=', float(self.__ui4.StepsPerRevolution.text()),
            'ipAdress=', str(self.__ui4.ipAdress.text()), 'illuminationTime=', float(self.__ui4.illuminationTime.text()),
            'illuminationIntensity=', float(self.__ui4.illuminationIntensity.text()), 'PrinterLiquidPrice=', float(self.__ui4.PrinterLiquidPrice.text())]
        json.dump(SettingsList, configfile)
        configfile.close()

        self.__printerSettings.close() #closes the window

    def loadPrinterSettings(self):

        configfile = open('PrinterSettings.conf', 'r')
        SettingsList=json.load(configfile)

        self.__ui4.AreaWidth.clear()
        self.__ui4.AreaWidth.insert('%d' % SettingsList[1])
        self.__ui4.AreaLength.clear()
        self.__ui4.AreaLength.insert('%d' % SettingsList[3])
        self.__ui4.AreaHeight.clear()
        self.__ui4.AreaHeight.insert('%d' % SettingsList[5])
        self.__ui4.HeightPerRevolution.clear()
        self.__ui4.HeightPerRevolution.insert('%d' % SettingsList[7])
        self.__ui4.StepsPerRevolution.clear()
        self.__ui4.StepsPerRevolution.insert('%d' % SettingsList[9])
        self.__ui4.ipAdress.clear()
        self.__ui4.ipAdress.insert(SettingsList[11])
        self.__ui4.illuminationTime.clear()
        self.__ui4.illuminationTime.insert('%d' % SettingsList[13])
        self.__ui4.illuminationIntensity.clear()
        self.__ui4.illuminationIntensity.insert('%d' % SettingsList[15])
        self.__ui4.PrinterLiquidPrice.clear()
        self.__ui4.PrinterLiquidPrice.insert('%d' % SettingsList[17])

        configfile.close()

    def MoveStepper(up=True, no_of_steps=1): #This is going to be the motor step function
        print up
        print no_of_steps

    def MoveStepperToEndPos(self,Endposition=True):
        #False is Startposition
        pass

    def ManualPrintingAbort(self):
        w = QWidget()
        QMessageBox.critical(w, 'Message', 'Printing stopped by user!')
        self.MoveStepperToEndPos(True)
        self.__printingWindow.close()
        self.__mainWindow.show()

    def fileDialogFunction(self):
        filename = QFileDialog.getOpenFileName(self.__mainWindow, 'Open File') #LINUX
        #filename = QFileDialog.getOpenFileName(mainWindow, 'Open File', 'C:\') #WINDOWS
        print("")
        print("filepath: " + str(filename))

        if filename.contains(".stl") > -1:
            self.__stl_model.open(filename)

            if not self.__stl_view is None:
                self.__glMain.delDrawable(self.__stl_view)

            self.__stl_view = StlModelView(self.__stl_model)
            scale = self.__stl_view.scale

            self.__glMain.reset()

            if scale > -1:
                self.__glMain.scale = scale
                print("new scale:" + str(scale))
            else:
                print("no new scale")

            self.__glMain.addDrawable(self.__stl_view)
            self.__glMain.update()


    def sendToRaspberry(self):
        configfile = open('PrinterSettings.conf', 'r')
        SettingsList=json.load(configfile)
        configfile.close()

        sentFile = {'file': ('../View/PrinterSettings.conf', open('../View/PrinterSettings.conf', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
        r1 = requests.post(str(SettingsList[11]) + ":/home/pi/printerData", files=sentFile)
        r2 = requests.post(str(SettingsList[11]) + ":/home/pi/printerData", data=str(SettingsList))


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
        self.__ui2.OkButton.clicked.connect(self.switchToPrintingMode)
        self.__ui2.CancelButton.clicked.connect(self.__printingDialog.close)

        #Explaining what each button on the PrintingWindow does
        self.__ui3.StopPrintButton.clicked.connect(self.ManualPrintingAbort)

        #Explaining what each button on the  printingSettingsWindow does
        if os.path.isfile('PrinterSettings.conf'):
            self.loadPrinterSettings()

        self.__ui4.CancelButton.clicked.connect(self.__printerSettings.close)
        self.__ui4.OkButton.clicked.connect(self.savePrinterSettingsToFile)
