__author__ = 'aslan'

import json
from StlModels import StlModel
from abc import ABCMeta,abstractmethod
from Compression import compressFileToString
import base64

class SerializablePackage(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def json(self):
        pass




class PrintingTask(SerializablePackage):

    def __init__(self):

        self.slices = None
        self.step_width = -1
        self.exposure_time = -1
        self.stl_model = None


    def is_valid(self):

        valid = self.slices is not None and self.step_width >= 0 and self.exposure_time >0
        valid = valid and self.stl_model is not None and isinstance(self.stl_model, StlModel)

        return valid


    def __str__(self):
        return str(self.json())


    def json(self):

        dict = {}

        if self.is_valid():



            dict['step_width'] = self.step_width
            dict['exposure_time'] = self.exposure_time
            #dict['stl_file'] =

            slices = []

            for s in self.slices:
                slices.append(s.points)

            dict['slices'] = slices

            file = open(self.stl_model.path, 'r')
            dict['stl_file'] = base64.encodestring(compressFileToString(file))


        return json.dumps(dict)





if __name__=="__main__":

    from SlicingModels import EquiSlicer, Slice

    stl_model = StlModel("../Data/pimpstickv2.stl")
    slices = EquiSlicer(stl_model).slice()

    task = PrintingTask()
    task.stl_model = stl_model
    task.slices = slices
    task.step_width = 4
    task.exposure_time = 2

    print(task.is_valid())

    print(task.json())









