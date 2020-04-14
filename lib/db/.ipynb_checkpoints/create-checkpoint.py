import pymongo
import pandas as pd
import re
import os
import time
from stat import *


def skipNAKV(X): 
    return {k:v for k,v in X.iteritems() if v}

def skipNA(X): 
    return [i for i in X if i == i]

def calcTreatmentConc(x,):
    """Input row sample information """
    return x.aliquot_concentration * x.dilution_factor/200

def create_study(name,col_study=None,
                 replace=False,
                 cell=None,tech='TempOSeq',src='BioSpyder',media=None,
                 times_hr=[],trts=[],concs_um=[],nreps=[]
                ):
    if not col_study: return
    Study = col_study.find_one(dict(name=name))
    if replace:
        col_study.delete_one(dict(name=name))
    
    Study = dict(name=name,
             cell=cell,
             tech=tech,
             src =src,
             media=skipNA(media),
             times_hr=skipNA(times_hr),
             trts=trts,
             concs_um=skipNA(concs_um),
             nreps=nreps)

    col_study.insert_one(Study)
    
    return col_study.find_one(dict(name=name))

def get_fastqs(fastq_path,col_save=None):
    X = []
    for d,sd,F in os.walk(fastq_path):
        if not F: continue
        for f in F:
            if not f.find('fastq')>-1: continue
            ST = os.stat(d+'/'+f)
            X.append([d,f,time.asctime(time.localtime(ST[ST_MTIME]))])
    FF = pd.DataFrame(X,columns=['path','fastq','mtime']).sort_values('mtime')
    FF['plate_id']=FF.fastq.str.replace('.fastq','').str.split('_').apply(lambda x: x[0])
    FF['well_id']=FF.fastq.str.replace('.fastq','').str.split('_').apply(lambda x: x[1])
    FF['mtime']=pd.to_datetime(FF.mtime)
    FF['well_id']=FF.well_id.apply(lambda x: re.sub('(\w+)0(\d+)','\\1\\2',x))
    FF['sample_id'] = FF['plate_id'] + '_' + FF['sample_id']
    
    if col_save:
        col_save.insert_many(FF.to_dict('records'))
    else:
        return FF
    
def create_well_trt(X,col_save=None,drop=False):
    """Input DF with following columns:
    ['sample_id',
     'block_id',
      'plate_id',
      'block_number',
      'well_id',
      'stype', 
      'name',
      'media',
      'timeh',
      'conc'
      ]
    """
    C =  ['sample_id',
          'block_id',
          'plate_id',
          'well_id',
          'stype', 
          'name',
          'media',
          'timeh',
          'conc'
          ]

    if len(X.columns.intersection(C))!=len(C) or not col_save: 
        print "column mismatch"
        return
    
    if drop:
        col_save.drop()
        col_save.insert_many(X[C].drop_duplicates().to_dict('record'))
    else:
        for x in X[C].drop_duplicates().to_dict('record'):
            y = col_save.find_one(x)
            if not y:
                col_save.insert_one(x)
            
    