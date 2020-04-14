import pandas as pd
import numpy as np
import re
import os
import time
import pylab as pl

def getCMapGeneSig(trt_id,dbc=None,fpn='fp_z1'):
    X = dbc.find_one(dict(trt_id=trt_id))
    if not X: return
    FP = X[fpn]
    Ch = FP['ch']['ds']
    Up = FP['up']['ds']
    Dn = FP['dn']['ds']
    
    return dict(ch=Ch,up=Up,dn=Dn)

def getBSPGeneZScore(name,trt_id=None,media=None,timeh=None,
                     conc=None,dbc=None,p0=None):
    if trt_id:
        X = dbc.find_one(dict(trt_id=trt_id))
    else:
        X = dbc.find_one(dict(name=name,media=media,timeh=timeh,conc=conc))
        
    if not X: return
    Z = pd.DataFrame(X['fcz'])
    if p0:
        Z = Z[Z.p<p0]
        
    Z['gene']=[i[0] for i in Z.probe_id.str.split('_')]
    # There will be multiple probes per gene
    
    return Z.groupby('gene').aggregate(dict(z=np.max))

def getCMapGeneZScore(trt_id,dbc=None):
    X = dbc.find_one(dict(trt_id=trt_id))
    if not X: return
    
    return pd.DataFrame(X['fpq_z'])\
            .sort_values(['z'],ascending=False)\
            .set_index('gene')
