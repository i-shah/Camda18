# %load ../env.py
%load_ext autoreload
%autoreload 2
%pylab inline
%matplotlib inline
#%load_ext rpy2.ipython

import matplotlib.text as text
import pandas as pd
import numpy as np
import pylab as pl
import scipy as sp
import sys
import rpy2 
from rpy2.robjects import r, pandas2ri
import os 
from sklearn.metrics.pairwise import euclidean_distances,manhattan_distances,cosine_similarity

#Set environment variables


# Set up the local source files
#TOP = os.getcwd().replace('notebooks','')
TOP = "/home/ishah/ipynb/Camda18/"

LIB = TOP+'lib'
if not LIB in sys.path: 
    sys.path.insert(0,LIB)

os.environ['PYTHONPATH']=LIB


DAT_DIR = TOP + '/data/'
FIG_DIR = TOP + '/figs/'

CMAP_DIR= '/share/home/ishah/projects/HTTR/data/'
CMAP_DAT= '/mnt/data/CMap/CMap2.0/CEL1/'

from db.mongo import *
#DB=openMongo(db='httr_ph1',host='pb.epa.gov')
#DB1=openMongo(db='httr_v1',host='pb.epa.gov')
#MSG=openMongo(db='msigdb_v6',host='pb.epa.gov')
#CMP=openMongo(db='cmap_v2',host='localhost')
CMP = pymongo.MongoClient("mongodb://localhost/cmap_v2")['cmap_v2']
#from gexp.deseq2 import *
pd.options.display.max_colwidth = 500
