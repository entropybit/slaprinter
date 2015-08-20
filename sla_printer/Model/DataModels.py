__author__ = 'mithrawnuruodo'


from datetime import datetime

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
        return "[" + self.timestamp + "]" + "raw data object: " + str(self.data)


class SlicesData(Data):

    def __init__(self, slices):

        Data.__init__()

