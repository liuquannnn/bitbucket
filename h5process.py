import sys
import os
from PIL import Image
from scipy.misc import imshow
from scipy.misc import toimage
from metpy.plots.ctables import registry
import matplotlib.pyplot as plt
import numpy as np
from metpy.plots import ctables
import matplotlib as mpl
from PIL import Image

STRIDE = 32
PADDING = 0
FIELDSIZE = 64
FILEMODEL = 'BMP'

def grbprocess(infile, feature, lat1, lon1, lat2, lon2, roci) :
    grbs = pygrib.open(infile)
    try:
        precipitable_water = grbs.select(name = 'Precipitable water')[0]
    except:
        print "can't find precipitable water"
    
#    wind_speed_gust = grbs.select(name = 'Wind speed (gust)')[0]
    timestamp = str(precipitable_water.dataDate) + "{0:0=4}".format(precipitable_water.dataTime)
#    print 'timestamp', timestamp
    lats, lons = precipitable_water.latlons()
#    print 'latitude info', lats.shape, lats.min(), lats.max()
#    print 'longitude info',lons.shape, lons.min(), lons.max()
    data, lats, lons = precipitable_water.data(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2)
#    print 'crop info', data.shape, lats.min(), lats.max(), lons.min(), lons.max()

#    data = data*1000
#    data /= 255.0
#    data = data.astype(int)

#   scipy image processing
#    print data
#    slidingwindow(data, timestamp)

#    imshow(data)
#    img = toimage(data)
    return data, timestamp
   
#get some color tables from metpy
#    wv_norm, wv_cmap = registry.get_with_steps('WVCIMSS', 0, 1)
#    data = wv_cmap(data, bytes=True)
#    imshow (colordata)


#    img = Image.fromarray(data)
#    img.save('test.bmp', format = 'BMP')

def slidingwindow (data, data_info, path):

#    print data.shape
#    print list(pd)
    index_max = (data.shape[1] - FIELDSIZE)/STRIDE + 1
    edge = (data.shape[1] - (index_max + 1) * STRIDE) / 2
#    print index_max
    count_t = 0
    count_f = 0
    for index in range(0, data.shape[0]):
        for row in xrange (edge, index_max*STRIDE + edge, STRIDE):
            for column in xrange(edge, index_max*STRIDE + edge, STRIDE):
#            print 'row index = ' row, ' column index = 'column
#             filename = timestamp + "{0:0=3}".format(row) + "{0:0=3}".format(column)+ '.' + FILEMODEL
                filename = data_info["time"][index] + "{0:0=3}".format(row) + "{0:0=3}".format(column)
                windows = data [index, row:row + FIELDSIZE, column:column + FIELDSIZE] #fix python slicing excluding the end index

            
                if (row == index_max * STRIDE / 2 + edge and column == index_max * STRIDE / 2 + edge):
#                print row, column
#                plt.imshow(windows)
#                plt.show()
                    outputgrayimage(windows[:,:,0], filename + 'IR1.' + FILEMODEL, path + 'IR1/1')
                    outputgrayimage(windows[:,:,1], filename + 'WV.' + FILEMODEL, path + 'WV/1')
                    outputgrayimage(windows[:,:,2], filename + 'VIS.' + FILEMODEL, path + 'VIS/1')
                    outputgrayimage(windows[:,:,3], filename + 'PMW.' + FILEMODEL, path + 'PMW/1')
                    count_t +=1
                else:
                    outputgrayimage(windows[:,:,0], filename + 'IR1.' + FILEMODEL, path + 'IR1/0')
                    outputgrayimage(windows[:,:,1], filename + 'WV.' + FILEMODEL, path + 'WV/0')
                    outputgrayimage(windows[:,:,2], filename + 'VIS.' + FILEMODEL, path + 'VIS/0')
                    outputgrayimage(windows[:,:,3], filename + 'PMW.' + FILEMODEL, path + 'PMW/0')
                    count_f +=1
#            imshow(windows)
    print "true", count_t, "false", count_f


def predictslidingwindow (data, timestamp, path):

#    print data.shape
#    print timestamp
#    print path
#    print list(pd)
    index_max = (data.shape[0] - FIELDSIZE)/STRIDE + 1
#    print index_max
    count = 0
    for row in xrange (0, index_max*STRIDE, STRIDE):
        for column in xrange(0, index_max*STRIDE, STRIDE):
            print 'row index = ' , row, ' column index = ', column
#             filename = timestamp + "{0:0=3}".format(row) + "{0:0=3}".format(column)+ '.' + FILEMODEL
            filename = timestamp + "{0:0=3}".format(row) + "{0:0=3}".format(column)
            windows = data [row:row + FIELDSIZE, column:column + FIELDSIZE] #fix python slicing excluding the end index
            print windows.shape
            print filename
#            print windows
            outputcolorimage(windows, filename + '.' + FILEMODEL, path )
            count +=1
            print count

    print timestamp, "total exmpale", count



def outputnumpy(windows, filename, path):
    np.save(path + '/' + filename, windows)
    # compressed with zip
#    np.savez_compressed(path + '/' + filename, windows)


def outputgrayimage(windows, filename, path):

    img = toimage(windows)
    img.save(path + '/' + filename, format = FILEMODEL, quality = 95)


def outputcolorimage(windows, filename, path):

#    img = toimage(windows)
#    img.save(path + '/' + filename, format = FILEMODEL)
#    wv_norm, wv_cmap = ctables.registry.get_with_steps('WVCIMSS', 0, 1)
    wv_norm, wv_cmap = ctables.registry.get_with_steps('wv_tpc', 0, 1)
    norm = mpl.colors.Normalize()
    windows =  norm(windows)
#    im = plt.imshow(windows, cmap=wv_cmap)
#    plt.show()
    img = Image.fromarray(wv_cmap(windows, bytes=True))
    img.save(path + '/' + filename, format = FILEMODEL, quality = 95)