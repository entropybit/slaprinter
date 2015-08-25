__author__ = 'mithrawnuruodo'

import json

class ConfigurationModel(object):

    def __init__(self):
        self.__server_ip = ""
        self.__ssl = False

        # geometric settings
        self.__width = 0.0
        self.__length = 0.0
        self.__height = 0.0
        self.__height_per_rev = 0.0
        self.__steps_per_rev = 0.0

        # illumination
        self.__illumination_time = 0.0
        self.__illumination_intensity = 0.0

        # fluid properties
        self.__liquid_price = 0.0

    def parse(self, list):
        #print(list)

        self.__width = float(list[1])
        self.__length = float(list[3])
        self.__height = float(list[5])

        self.__height_per_rev = float(list[7])
        self.__steps_per_rev = float(list[9])

        self.__server_ip = str(list[11])


        self.__illumination_time = float(list[13])
        self.__illumination_intensity = float(list[15])
        self.__liquid_price = float(list[17])

        #self.__ssl = str(list[19])


    def save(self, path='PrinterSettings.conf'):


        configfile = open(path, 'w')
        SettingsList= [
            'AreaWidth=', self.__width,
            'AreaLength=', self.__length,
            'AreaHeight=', self.__height,
            'HeightPerRevolution=', self.__height_per_rev,
            'StepsPerRevolution=', self.__steps_per_rev,
            'ipAdress=', self.__server_ip,
            'illuminationTime=', self.__illumination_time,
            'illuminationIntensity=', self.__illumination_intensity,
            'PrinterLiquidPrice=', self.__liquid_price
        ]
        json.dump(SettingsList, configfile)
        configfile.close()


    @property
    def server_ip(self):
        return self.__server_ip

    @property
    def width(self):
        return self.__width

    @property
    def length(self):
        return self.__length

    @property
    def height(self):
        return self.__height

    @property
    def height_per_rev(self):
        return self.__height_per_rev

    @property
    def steps_per_rev(self):
        return self.__steps_per_rev

    @property
    def illumination_time(self):
        return self.__illumination_time

    @property
    def illumination_intentsity(self):
        return self.__illumination_intensity

    @property
    def liquid_price(self):
        return self.__liquid_price

    @property
    def ssl(self):
        return self.__ssl

    @server_ip.setter
    def server_ip(self,ip):
        self.__server_ip = ip

    @width.setter
    def width(self, width):
        self.__width = width

    @height.setter
    def height(self, height):
        self.__height = height

    @length.setter
    def length(self, length):
        self.__length = length

    @height_per_rev.setter
    def height_per_rev(self,height_per_rev):
        self.__height_per_rev = height_per_rev

    @steps_per_rev.setter
    def steps_per_rev(self,steps_per_rev):
        self.__steps_per_rev = steps_per_rev

    @illumination_intentsity.setter
    def illumination_intentsity(self,intensity):
        self.__illumination_intensity = intensity

    @illumination_time.setter
    def illumination_time(self,time):
        self.__illumination_time = time

    @liquid_price.setter
    def liquid_price(self,price):
        self.__liquid_price = price

    @ssl.setter
    def ssl(self,ssl_flag):
        self.__ssl = ssl_flag


if __name__=="__main__":

    c = ConfigurationModel()
    c.width = 18.0
    c.height = 18.8
    c.length = 10.0
    c.illumination_intentsity = 10.0
    c.illumination_time = 10.0
    c.server_ip = "10.0.0.1"
    c.liquid_price = 201.18
    print(c.ssl)
    print(c.illumination_intentsity)
