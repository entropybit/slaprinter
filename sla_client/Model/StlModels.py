__author__ = 'mithrawnuruodo'


from stl import mesh

class StlModel(object):

    def __init__(self, path=""):


        self.mesh = None

        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0
        self.z_min = 0
        self.z_max = 0

        if path != "":
            self.open(path)

    def open(self,path):
        self.mesh = mesh.Mesh.from_file(path)
        self.analyse()


    def analyse(self):

        n = len(self.mesh)

        v0s = self.mesh.v0
        v1s = self.mesh.v1
        v2s = self.mesh.v2

        for i in range(0,n):

            v0 = v0s[i]
            v1 = v1s[i]
            v2 = v2s[i]

            if i == 0:
                self.x_max = v0[0]
                self.x_min = v0[0]

                self.y_max = v0[1]
                self.y_min = v0[1]

                self.z_max = v0[2]
                self.z_min = v0[2]

            self.update_all_minmax(v0)
            self.update_all_minmax(v1)
            self.update_all_minmax(v2)

        print("x \in [" + str(self.x_min) + ", " + str(self.x_max)+"]")
        print("y \in [" + str(self.y_min) + ", " + str(self.y_max)+"]")
        print("z \in [" + str(self.z_min) + ", " + str(self.z_max)+"]")


    def update_all_minmax(self,v):

        x = v[0]
        y = v[1]
        z = v[2]

        self.x_min, self.x_max = self.update_minmax(x, self.x_min, self.x_max)
        self.y_min, self.y_max = self.update_minmax(y, self.y_min, self.y_max)
        self.z_min, self.z_max = self.update_minmax(z, self.z_min, self.z_max)




    def update_minmax(self, x, xmin, xmax):

        if x > xmax:
            xmax = x
        else:
            if x <= xmin:
                xmin = x


        return [xmin, xmax]


    @property
    def xlims(self):

        return [self.x_min, self.x_max]


    @property
    def ylims(self):

        return [self.y_min, self.y_max]


    @property
    def zlims(self):

        return [self.z_min, self.z_max]






