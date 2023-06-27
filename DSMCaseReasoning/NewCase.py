from osgeo import gdal
import numpy as np
import math
class NewCase:
    #init
    def __init__(self):
        self.__up = 0
        self.__down = 10
        self.__resolution = 85
        self.__property = 15
        self.__area = 25286
        self.__SDH = 338
        self.__meanS = 9
        self.__elevationD = 3313

    @classmethod
    def from_DEMfile(cls, up, down, property, DEMfile):
        obj = cls()
        obj.__up = up
        obj.__down = down
        obj.__property = property
        obj.__DEMfile = DEMfile

        obj.__resolution = obj.calculate_resolution()
        obj.__area = obj.calculate_area()
        obj.__SDH = obj.calculate_SDH()
        obj.__meanS = obj.calculate_meanS()
        obj.__elevationD = obj.calculate_elevationD()

        return obj

    def set_up(self, up):
        self.__up = up

    def set_down(self, down):
        self.__down = down

    def set_property(self, property):
        self.__property = property

    def set_resolution(self, resolution):
        self.__resolution = resolution

    def set_area(self, area):
        self.__area = area

    def set_SDH(self, SDH):
        self.__SDH = SDH

    def set_meanS(self, meanS):
        self.__meanS = meanS

    def set_elevationD(self, elevationD):
        self.__elevationD = elevationD

    def set_DEMfile(self, DEMfile):
        self.__DEMfile = DEMfile
        '''
        self.__resolution = self.calculate_resolution()
        self.__area = self.calculate_area()
        self.__SDH = self.calculate_SDH()
        self.__meanS = self.calculate_meanS()
        self.__elevationD = self.calculate_elevationD()
        '''
    # get value of variable
    def get_up(self):
        return self.__up

    def get_down(self):
        return self.__down

    def get_property(self):
        return self.__property

    def get_DEMfile(self):
        return self.__DEMfile

    def get_resolution(self):
        return self.__resolution

    def get_area(self):
        return self.__area

    def get_SDH(self):
        return self.__SDH

    def get_meanS(self):
        return self.__meanS

    def get_elevationD(self):
        return self.__elevationD

    # calculate the resolution of DEM
    def calculate_resolution(self):
        dem = gdal.Open(self.__DEMfile)
        geotransform = dem.GetGeoTransform()
        resolution_x = geotransform[1]
        resolution_y = geotransform[5]
        return (abs(resolution_x) + abs(resolution_y)) / 2

    # calculate total area of DEM
    def calculate_area(self):
        # open DEM
        dem = gdal.Open(self.__DEMfile)
        band = dem.GetRasterBand(1)
        dem_array = dem.ReadAsArray()
        geotransform = dem.GetGeoTransform()
        resolution_x = geotransform[1]
        resolution_y = geotransform[5]

        valid_pixels = np.count_nonzero(dem_array != band.GetNoDataValue())
        area = valid_pixels * abs(resolution_x) * abs(resolution_y)/ (1000**2)

        return area

    def calculate_SDH(self):

        dem = gdal.Open(self.__DEMfile)
        band = dem.GetRasterBand(1)
        nodata = band.GetNoDataValue()
        #read DEM data
        dem_array = dem.ReadAsArray()
        rows, cols = dem_array.shape

        sdh_array = np.zeros((rows, cols))

        #calculate SDH by 3*3 window
        for i in range(rows):
            for j in range(cols):
                elevation = dem_array[i][j]
                # valid data or on the border
                if elevation != nodata and i > 0 and i < rows - 1 and j > 0 and j < cols - 1:
                    elevation = np.zeros(9)
                    t = 0
                    flag = 1
                    for p in range(-1, 2):
                        for q in range(-1, 2):
                            if dem_array[i+p][j+q] != nodata:
                                elevation[t]=float(dem_array[i+p][j+q])
                                t = t+1
                            else:
                                flag = 0
                    #if not on the edge of inner NoData area
                    if flag==1 :
                        elevation_max = np.max(elevation)
                        elevation_min = np.min(elevation)
                        sdh = elevation_max-elevation_min
                        sdh_array[i][j] = sdh
        # total sdh
        sdh_mean = np.true_divide(sdh_array.sum(), (sdh_array != 0).sum())
        return sdh_mean

    # calculate mean slope
    def calculate_meanS(self):
        # open DEM
        dem = gdal.Open(self.__DEMfile)
        geotransform = dem.GetGeoTransform()
        resolution_x = geotransform[1]
        resolution_y = geotransform[5]
        band = dem.GetRasterBand(1)
        nodata = band.GetNoDataValue()
        # read DEM data
        dem_array = dem.ReadAsArray()
        rows, cols = dem_array.shape

        slope_array = np.zeros((rows, cols))
        # calculate slop by 3*3 window
        for i in range(rows):
            for j in range(cols):
                elevation = dem_array[i][j]
                if elevation != nodata and i > 0 and i < rows - 1 and j > 0 and j < cols - 1:
                    elevation = np.zeros(9)
                    t = 0
                    flag = 1
                    for q in range(-1, 2):
                        for p in range(-1, 2):
                            if dem_array[i + p][j + q] != nodata:
                                elevation[t] = float(dem_array[i + p][j + q])
                                t = t + 1
                            else:
                                flag = 0

                    if flag == 1:
                        dz_dx = (elevation[6] + 2 * elevation[7] + elevation[8] - elevation[0] - 2 * elevation[1] - elevation[2]) / (
                                            8 * resolution_x)
                        dz_dy = (elevation[2] + 2 * elevation[5] + elevation[8] - elevation[0] - 2 * elevation[3] - elevation[6]) / (
                                            8 * resolution_y)
                        slope = np.sqrt(dz_dx ** 2 + dz_dy ** 2)
                        slope_degree = math.atan(slope) * 180 / math.pi
                        slope_array[i][j] = slope_degree

        slope_mean = np.true_divide(slope_array.sum(), (slope_array != 0).sum())
        return slope_mean

    # calculate elevation difference
    def calculate_elevationD(self):
        # open DEMfile
        dem = gdal.Open(self.__DEMfile)
        # read DEM data
        dem_array = dem.ReadAsArray()
        # get the first band of DEM
        band = dem.GetRasterBand(1)
        max_elevation = np.max(dem_array[dem_array != band.GetNoDataValue()])
        min_elevation = np.min(dem_array[dem_array != band.GetNoDataValue()])
        elevation_diff = max_elevation - min_elevation

        return elevation_diff
