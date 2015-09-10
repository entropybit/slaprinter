__author__ = 'mithrawnuruodo'


from datetime import datetime
import numpy as np

class Data(object):

    uuids = []

    def __init__(self):

        if len(self.uuids) == 0:
            self.uuid = 1

        else:
            self.uuid = self.uuids[-1] + 1

        self.uuids.append(self.uuid)
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        self.__timestamp = now

    def __hash__(self):
        return self.uuid

    @property
    def timestamp(self):
        return self.__timestamp


class RawData(Data):

    def __init__(self, data):
        Data.__init__(self)
        self.__data = data

    @property
    def data(self):
        return  self.__data


    def __str__(self):
        return "[" + self.timestamp + "] raw data object: " + str(self.data)


class PrintingTaskData(Data):

    def __init__(self):

        Data.__init__(self)


        self.slices = None
        self.slice_number = 0
        self.stl_file = None
        self.step_width = -1
        self.illumination_time = -1
        self.illumination_intensity = -1
        self.stl_model = None
        self.finished = False
        self.slices_todo = None
        self.file_name = ""



    def is_valid(self,json_dump):

        valid = 'step_width' in json_dump and 'illumination_time' in json_dump and 'illumination_intensity' in json_dump
        valid = valid and 'slices' in json_dump and 'slice_number' in json_dump
        valid = valid and 'stl_file' in json_dump and 'file_name' in json_dump

        return valid


    def __str__(self):
        return "[" + self.timestamp + "] printing task data object: " + str(self.file_name)


    def parse(self, json_dump):


        valid = self.is_valid(json_dump)

        if valid:

            self.step_width = float(json_dump["step_width"])
            self.illumination_time = float(json_dump["illumination_time"])
            self.illumination_intensity = float(json_dump["illumination_intensity"])

            self.slices = json_dump["slices"]
            self.slices_todo = list(np.zeros(len(self.slices), dtype=bool))

            self. slice_number = int(json_dump["slice_number"])

            self.stl_file = json_dump["stl_file"]
            self.file_name = json_dump["file_name"]


        return valid


    @property
    def time(self):
        ts = self.timestamp
        ts = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")

        now = datetime.now()

        diff = now - ts

        [mins, secs] = divmod(diff.days * 86400 + diff.seconds, 60)

        return str(mins) + "mins " + str(secs) + "s ago"








