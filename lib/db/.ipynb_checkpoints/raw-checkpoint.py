import db.mongo
import pandas as pd
import numpy as np

Filt0 = dict(_id=0,dsstox_sid=1,media=1,timeh=1,bspd_plate_id=1,plate_id=1,
             well_id=1,name=1,conc=1,probe_cnts=1,stype=1)

Ind0 = ['dsstox_sid', 'name', 'media', 'well_id', 'conc', 'timeh', 'plate_id', 
        'bspd_plate_id', 'stype']

def loadRawChemDataForDESeq(*args,**kwargs):
    """
    Args:
    chems: list of chemical names (mostly just one)
    dbc  : mongo collection httr_v1.httr_well
    
    KWArgs:
    media: media condition
    timeh: time point
    ctrl : the stype for the control samples (default='vehicle control')
    
    """

    Trt,Cnt = loadRawChemProfiles(*args,**kwargs)
    SID=Trt['plate_id']+'_'+Trt['well_id']
    Cnt['sample_id']=list(SID)
    Trt['sample_id']=list(SID)
    Trt.name.fillna('DMSO',inplace=True)
    Trt['trt_id'] = Trt.name+'__'+Trt.conc.astype(np.str_)
    Trt.set_index('sample_id',inplace=True)
    Cnt.set_index('sample_id',inplace=True)

    return Trt,Cnt

    
def loadRawChemProfiles(chems,dbc,media=None,timeh=None,ctrl=['vehicle control'],
                       nrm=False,dbg=False):
    """
    Args:
    chems: list of chemical names (mostly just one)
    dbc  : mongo collection httr_v1.httr_well
    
    KWArgs:
    media: media condition
    timeh: time point
    ctrl : the list of stype(s) for the control samples (default='vehicle control')
    nrm  : normalize ? True or False
    
    """
    
    x_cnts = 'probe_cnts_nrm' if nrm else 'probe_cnts'
    
    Filt0 = dict(_id=0,media=1,timeh=1,plate_id=1,
                 well_id=1,name=1,conc=1,stype=1)
    Filt0[x_cnts]=1
    
    Ind0 = [ 'name', 'media', 'well_id', 'conc', 'timeh', 'plate_id', 
            'stype']


    Q0 = {'name':{'$in':chems}}
    if media: Q0['media']=media
    if timeh: Q0['timeh']=timeh
    
    # Find plate ids with these samples
    PID = dbc.find(Q0).distinct('plate_id')
    
    if dbg: print ("Plates: %s" % ",".join(PID))
    
    # Load the chemical treatments
    
    R0 = []
    
    for X in dbc.find(Q0,Filt0):
        pc = X.pop(x_cnts)
        X.update(pc)
        R0.append(pd.Series(X))
        
    # Now load the controls 
    if ctrl:
        Q1 ={'plate_id':{'$in':PID},'stype':{'$in':ctrl}}
        if media: Q1['media']=media
        if timeh: Q1['timeh']=timeh
        
        for X in dbc.find(Q1,Filt0):
            pc = X.pop(x_cnts)
            X.update(pc)
            R0.append(pd.Series(X))
    
    if len(R0)==0: return
    
    R1 = pd.DataFrame(R0)
    Trt = R1[Ind0]
    Trt.conc.fillna(0,inplace=True)
    
    return Trt,R1.drop(Ind0,axis=1).fillna(0)
