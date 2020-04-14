import pymongo
import pandas as pd
import re
import os
import time
from stat import *
import numpy as np

def get_cels(cel_path):
    X = []
    for d,sd,F in os.walk(cel_path, followlinks=True):
        if not F: continue
        for f in F:
            if not re.search('cel$|cel.bz2$|cel.gz',f,re.I): continue
            ST = os.stat(d+'/'+f)
            X.append([d,f,time.asctime(time.localtime(ST[ST_MTIME]))])
    
    FF = pd.DataFrame(X,columns=['path','cel','mtime']).sort_values('mtime')
    return FF
