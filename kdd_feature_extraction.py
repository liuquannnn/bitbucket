from multiprocessing import Process, Pool
from h5process import grbprocess, slidingwindow
import matplotlib.pyplot as plt
from glob import glob
import sys
import os
import datetime
import numpy as np
import pandas as pd
import h5py



FEATURE = 'Circular'
file = "/Data/weather/yuju/Year.2010.ibtracs_all.v03r10.csv"


# where to find kdd data
basedir = "/Data/KDD/TCIR-ALL_2017.h5"

outdir = "/Data/KDD/"

outdir_IR1 = outdir + 'IR1/'
outdir_WV  = outdir + 'WV/'
outdir_VIS = outdir + 'VIS/'
outdir_PMW = outdir + 'PMW/'
folderlist = [outdir_IR1, outdir_WV, outdir_VIS, outdir_PMW]


def process(filename):
    info('function process')
    print filename
    try:
        data_info = pd.read_hdf(filename, key="info", mode='r')

        # load "matrix" as numpy ndarray, this could take longer times
        with h5py.File(filename, 'r') as hf:
            data_matrix = hf['matrix'][:]
    except:
        print "Fail to access GFS data"
  
    return data_matrix

def info(title):
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):  # only available on Unix
        print 'parent process:', os.getppid()
    print 'process id:', os.getpid()

def f(x):
    info('function f')
    print x

def extract(feature_matrix):
    for feature in feature_matrix：
        for i in range(4):
            efeature = feature[:,:,i]
            a = []
            fifeature = []
            for theta in xrange(0,6 * math.pi, 0.01):
                r = 4.775 * theta
                int x = r * math.cos(theta) + 101
                int y = r * math.sin(theta) + 101
                efeature[x,y]
                if [x, y] not in a:
                    a.append([x, y])
            for x, y in a:
                fifeature.append(efeature[x, y])
            np.savetxt('feature.csv',fifeature,delimiter = ',')
    
    
if __name__ == '__main__':
    
    start_time = datetime.datetime.now()
    print start_time

    info('main line')

    for folder in folderlist:
        if not os.path.exists(folder):
            os.makedirs(folder)

    feature_matrix = np.asarray(process(basedir))
    
    print feature_matrix.shape
    
    extract(feature_matrix)
    
    end_time = datetime.datetime.now()
    print "start time is {0}, end time is {1}, execution time is {2}".format(start_time, end_time, (end_time - start_time))

