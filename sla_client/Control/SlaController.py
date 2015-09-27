__author__ = 'mithrawnuruodo'

from PyQt4.QtGui import QApplication, QMainWindow, QDialog, QWidget, QMessageBox, QFileDialog
from PyQt4 import QtCore
from View import Ui_MainWindow, GLWidget, Ui_PrinterSettings, Ui_PrintingDialog, Ui_PrintingWindow, StlModelView
from View import Ui_SlicingWindow, SliceModelView, PlaneCutView
from Model import StlModel, EquiSlicer, ConfigurationModel
#from Model import
import json, requests, time
import sys
import os.path
from ServerConnection import ServerConnection
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
        self.__slicing_model = None
        self.__slicing_view = None
        self.__slices = None
        self.__slicing_index = 0

        self.__connection = None
        self.__config = ConfigurationModel()
        self.current_z = 0

    def start(self):
        self.initWindows()
        self.makeConnections()
        self.__mainWindow.show()
        sys.exit(self.exec_())


    def initWindows(self):

        #self.connection.start()
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

        # initial settings load
        self.loadPrinterSettings()

    def init_printing_window(self):
        '''
            Initiating printing window
        '''
        #self.__glStatus = GLWidget()
        self.__ui3.setupUi(self.__printingWindow)
        #self.__ui3.OpenGlPanel.addWidget(self.__glMain)


    def init_slicing_window(self):
        '''
            Initializing slicing window
        '''
        self.__glSlice  = GLWidget()
        self.__glSlice.allow_rot = False
        self.__glSlice.allow_zoom = True
        #self.__glSlice.draw_frame = True

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
        self.__ui1.showCutButton.clicked.connect(self.showcut)


        self.__ui2.CancelButton.clicked.connect(self.__printingDialog.close)
        self.__ui2.OkButton.clicked.connect(self.switchToPrintingMode)



        self.__ui1.SlicingButton.clicked.connect(self.__slicingwindow.show)
        self.__ui1.SlicingButton.clicked.connect(self.doSlicing)
        #ui1.DownPosButton.clicked.connect(MoveStepper, [False,2])            #why cant i call functions with parameters?
        #ui1.UpPosButton.clicked.connect(MoveStepper(True, N))


        self.__ui4.OkButton.clicked.connect(self.savePrinterSettingsToFile)
        self.__ui4.CancelButton.clicked.connect(self.__printerSettings.close)

        self.__ui6.nextButton.clicked.connect(self.next_slice)
        self.__ui6.prevButton.clicked.connect(self.prev_slice)

    def switchToPrintingMode(self):

        self.__ui1.OpenGlPanel.removeWidget(self.__glMain)
        self.__mainWindow.close()
        self.__printerSettings.close() #shouldnt be open at this point, but you never know
        self.__printingDialog.close()
        self.__ui3.OpenGlPanel.addWidget(self.__glMain)
        self.__printingWindow.show()
        self.sendToRaspberry()

    def savePrinterSettingsToFile(self):

        # update values in config file
        self.__config.width = float(self.__ui4.AreaWidth.text())
        self.__config.length = float(self.__ui4.AreaLength.text())
        self.__config.height = float(self.__ui4.AreaHeight.text())

        self.__config.height_per_rev = float(self.__ui4.HeightPerRevolution.text())
        self.__config.steps_per_rev = float(self.__ui4.StepsPerRevolution.text())
        self.__config.server_ip = str(self.__ui4.ipAdress.text())
        #self.__config.ssl()
        self.__config.illumination_time = float(self.__ui4.illuminationTime.text())
        self.__config.illumination_intentsity = float(self.__ui4.illuminationIntensity.text())
        self.__config.liquid_price = float(self.__ui4.PrinterLiquidPrice.text())

        # save config to standard path
        self.__config.save()

        #close the window
        self.__printerSettings.close()

    def loadPrinterSettings(self):

        #ToDo: Implement this with a XML file

        configfile = open('PrinterSettings.conf', 'r')
        settings=json.load(configfile)

        # parse file to configuration object
        self.__config.parse(settings)


        self.__ui4.AreaWidth.clear()
        self.__ui4.AreaWidth.insert('%.2f' % self.__config.width)
        self.__ui4.AreaLength.clear()
        self.__ui4.AreaLength.insert('%.2f' % self.__config.length)
        self.__ui4.AreaHeight.clear()
        self.__ui4.AreaHeight.insert('%.2f' % self.__config.height)
        self.__ui4.HeightPerRevolution.clear()
        self.__ui4.HeightPerRevolution.insert('%.2f' % self.__config.height_per_rev)
        self.__ui4.StepsPerRevolution.clear()
        self.__ui4.StepsPerRevolution.insert('%.2f' % self.__config.steps_per_rev)
        self.__ui4.ipAdress.clear()
        self.__ui4.ipAdress.insert(self.__config.server_ip)
        self.__ui4.illuminationTime.clear()
        self.__ui4.illuminationTime.insert('%.2f' % self.__config.illumination_time)
        self.__ui4.illuminationIntensity.clear()
        self.__ui4.illuminationIntensity.insert('%.2f' % self.__config.illumination_intentsity)
        self.__ui4.PrinterLiquidPrice.clear()
        self.__ui4.PrinterLiquidPrice.insert('%.2f' % self.__config.liquid_price)

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

        if filename.contains(".stl"):
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
            self.__slicing_model = None
            self.__slices = None


    def sendToRaspberry(self):


        configfile = open('PrinterSettings.conf', 'r')
        # SettingsList=json.load(configfile)
        # configfile.close()
        #
        # sentFile = {'file': ('../View/PrinterSettings.conf', open('../View/PrinterSettings.conf', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
        # r1 = requests.post(str(SettingsList[11]) + ":/home/pi/printerData", files=sentFile)
        # r2 = requests.post(str(SettingsList[11]) + ":/home/pi/printerData", data=str(SettingsList))
        #
        #
        # #Explaining what each button on the PrintingDialog does
        # self.__ui2.OkButton.clicked.connect(self.switchToPrintingMode)
        # self.__ui2.CancelButton.clicked.connect(self.__printingDialog.close)
        #
        # #Explaining what each button on the PrintingWindow does
        # self.__ui3.StopPrintButton.clicked.connect(self.ManualPrintingAbort)
        #
        # #Explaining what each button on the  printingSettingsWindow does
        # if os.path.isfile('PrinterSettings.conf'):
        #     self.loadPrinterSettings()
        #
        # self.__ui4.CancelButton.clicked.connect(self.__printerSettings.close)
        # self.__ui4.OkButton.clicked.connect(self.savePrinterSettingsToFile)


    def doSlicing(self):

        # only slice if new model has been loaded
        if  self.__slices is None and self.__slicing_model is None:
            self.__slicing_model = EquiSlicer(self.__stl_model)
            self.__slices = self.__slicing_model.slice(100)

        slice = self.__slices[self.__slicing_index]
        scale = self.__slicing_model.scale

        self.__glSlice.update_scale(scale)


        #print(slice)

        n = len(self.__slices)

        s = "Equidistanc slicer used  n= " + str(n) + " slices have been created \n currently displaying slice ["
        s = s + str(self.__slicing_index+1) + "] \n "

        self.__ui6.algorithmLabel.setText(s)
        self.__slicing_view = SliceModelView(slice)
        self.__glSlice.addDrawable(self.__slicing_view)


    def next_slice(self):
        i = self.__slicing_index
        n = len(self.__slices)

        if i+1 <n:
            self.update_slice(i+1)


    def prev_slice(self):
        i = self.__slicing_index
        if i-1 >= 0:
            self.update_slice(i-1)

    def update_slice(self,i):

        slice = self.__slices[i]
        self.__slicing_index = i
        n = len(self.__slices)
        s = "Equidistanc slicer used  n= " + str(n) + " slices have been created \n currently displaying slice ["
        s = s + str(self.__slicing_index+1) + "] \n "

        #print("")
        #print("################################")
        #print("")
        #print(slice)
        #print("")
        #print("")
        #print("")

        self.__glSlice.delDrawable(self.__slicing_view)
        self.__ui6.algorithmLabel.setText(s)

        self.__slicing_view = SliceModelView(slice)
        self.__glSlice.addDrawable(self.__slicing_view)
        self.__glSlice.update()


    def showcut(self):

        x0, x1 = self.__stl_model.xlims
        y0, y1 = self.__stl_model.ylims

        dimx = x1-x0
        dimy = y1-y0

        self.current_z = float(self.__ui1.cutZCoordinate.text())
        self.__glMain.addDrawable(PlaneCutView(z=self.current_z, dimx=2*dimx, dimy=2*dimy, stl_model=self.__stl_model))
