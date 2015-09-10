__author__ = 'aslan'

import json
from StlModels import StlModel
from abc import ABCMeta,abstractmethod
from Compression import compressFileToString
import base64
import os
DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/Data"



class SerializablePackage(object):
    __metaclass__ = ABCMeta

    id = []

    def __init__(self, path=""):

        self._path = path

        if len(self.id) == 0:
            self.__id = 0
        else:
            self.__id = self.id[-1] + 1

        self.id.append(self.__id)

    def __hash__(self):
        return self.__id

    @abstractmethod
    def json(self):
        pass

    @property
    def path(self):
        return self._path




class PrintingTask(SerializablePackage):

    def __init__(self, path=""):

        SerializablePackage.__init__(self, path)
        self.slices = None



        self.step_width = -1
        self.illumination_time = -1
        self.illumination_intensity = -1
        self.stl_model = None


    def is_valid(self):

        valid = self.slices is not None and self.step_width >= 0 and self.illumination_time >0
        valid = valid and self.stl_model is not None and isinstance(self.stl_model, StlModel)
        valid = valid and self.illumination_intensity >0

        return valid


    def __str__(self):
        return str(self.json())


    def json(self):

        dict = {}

        if self.is_valid():



            dict['step_width'] = self.step_width
            dict['illumination_time'] = self.illumination_time
            dict['illumination_intensity'] = self.illumination_intensity
            dict['file_name'] = self.stl_model.filename
            #dict['stl_file'] =


            slice_number = 1
            slices = []

            for s in self.slices:
                points = []
                for line in s.points:
                    #print("line " + str(line))
                    l = [list(line[0]), list(line[1])]
                    points.append(l)
                slices.append(points)
                slice_number += 1
                #print("points")
                #print(points)

            #print(slices)
            dict['slices'] = slices
            dict['slice_number'] = slice_number

            file = open(self.stl_model.path, 'r')
            dict['stl_file'] = base64.encodestring(compressFileToString(file))


        return json.dumps(dict)





if __name__=="__main__":

    from SlicingModels import EquiSlicer, Slice
    import Control

    print("Data dir : " + DATA_DIR)


    import time

    #server = Control.ServerConnection("http://192.168.178.28/")
    server = Control.ServerConnection("http://127.0.0.1/")
    server.start()

    stl_model = StlModel(DATA_DIR + "/pimpstickv2.stl")
    #stl_model = StlModel("../Data/EiffelTowerTALL.stl")
    slices = EquiSlicer(stl_model).slice(30)

    task = PrintingTask(path="/post/task/")
    task.stl_model = stl_model
    task.slices = slices
    task.step_width = 4
    task.illumination_time = 2
    task.illumination_intensity = 1.28


    flag = isinstance(task, SerializablePackage)

    print("isinstance of SerializablePackage : " + str(flag))
    print("valid? : " + str(task.is_valid()))
    print("path: " + task.path)

    print(task.json())




    server.post_data(task)

    time.sleep(1.8)
    print("sleep over")
    server.stop()
    print("server stopped")







