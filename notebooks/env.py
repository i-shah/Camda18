%load_ext autoreload
%autoreload 2
%pylab inline
%matplotlib inline

import matplotlib.text as text
import pandas as pd
import numpy as np
import pylab as pl
import scipy as sp
import sys
import rpy2 
import os 
from sklearn.metrics.pairwise import euclidean_distances,manhattan_distances,cosine_similarity

#Set environment variables


# Set up the local source files
#TOP = os.getcwd().replace('notebooks','')
TOP = "/share/home/ishah/ipynb/chiron/Camda18/"

LIB = TOP+'lib'
if not LIB in sys.path: 
    sys.path.insert(0,LIB)

os.environ['PYTHONPATH']=LIB


DAT_DIR = TOP + '/data/'
FIG_DIR = TOP + '/figs/'

from db.mongo import *
from gexp.fc import *

#DB=openMongo(db='httr_ph1',host='pb.epa.gov')
#DB1=openMongo(db='httr_v1',host='pb.epa.gov')
MSG=openMongo(db='msigdb_v6',host='pb.epa.gov')
CMP=openMongo(db='cmap_v2',host='pb.epa.gov')
#from gexp.deseq2 import *
pd.options.display.max_colwidth = 500
