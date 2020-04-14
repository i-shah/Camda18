import db.mongo
import pandas as pd
import numpy as np

def saveDESeq2Res(FC,
                  ctrl='vehicle control',
                  meth='DESeq2',
                  dbc_trt_cmp=None,
                  dbc_save=None):
    """
    The DESeq2 results are for a single chemical all concentrations. The idea is to iterate 
    over each conc, link with trt_grp_cmp and store results.
    
    Args:
    FC:  pd.DataFrame containing the stats for each probe returned by .... At minimum this should include:
         probe_id, l2fc, p but can also include other information 
    ctrl: what samples were used as the control
    dbc_trt_cmp: mongo collection containing treatment groups
    dbc_save: mongo collection to store results
    """
    
    # Get the treatment group id
    
    if FC.shape[0]==0 or not dbc_trt_cmp or not dbc_save: return
    
    for (name,media,timeh,conc),X in FC.groupby(['name','media','timeh','conc']):
        trt_cmp_id = dbc_trt_cmp.find_one(dict(name=name,
                                               media=media,
                                               timeh=timeh,
                                               conc=conc,
                                               ctrl=ctrl
                                              ))['_id']
        Y = dict(name=name,media=media,timeh=timeh,conc=conc,
                 trt_grp_cmp_id=trt_cmp_id,
                 meth=meth,
                 degs=X.drop(['name','media','timeh','conc'],axis=1).to_dict('records'))
        
        dbc_save.insert_one(Y)


def loadFCChemProfiles1(chem,dbc_fc,meth='DESeq2',media=None,timeh=None,
                       conc=None,
                       p0=1.0,l2fc0=None):
    Q0 = dict(name=chem)
    if media: Q0['media']=media
    if timeh: Q0['timeh']=timeh
    if conc:  Q0['conc']=conc
    if meth: Q0['meth']=meth
    F0 = dict(_id=0,dsstox_sid=1,name=1,media=1,timeh=1,conc=1,
              degs=1,meth=1)
    I0 = [i for i in F0.keys() if i not in ['_id','degs']]
    X = []
    for x in dbc_fc.find(Q0,F0):
        fc = pd.DataFrame(x.pop('degs')).query("p<=%f" % p0)\
              .pivot_table(columns='probe_id',values='l2fc')
        for i in x.keys(): fc[i]=x[i]
        X.append(fc)
    
    FC = pd.DataFrame(X).set_index(I0).fillna(0)
    if l2fc0:
        N0 = (FC.abs()>l2fc0).sum(axis=0)
        J0 = N0[N0>0].index
        FC = FC[J0]
        
    return FC

def loadFCChemProfiles(chem,dbc_fc,meth='DESeq2',media=None,timeh=None,
                       conc=None,
                       p0=1.0,l2fc0=None,l2fc_se0=None):
    Q0 = dict(name=chem)
    if media: Q0['media']=media
    if timeh: Q0['timeh']=timeh
    if conc:  Q0['conc']=conc
    if meth: Q0['meth']=meth
        
    F0 = dict(_id=0,name=1,media=1,timeh=1,conc=1,
              degs=1,meth=1)
    I0 = [i for i in F0.keys() if i not in ['_id','degs']]
    Prb = []
    
    # Find significant probes (use aggregation for this in future)
    pf = "p<=%f and (l2fc<-%f or l2fc > %f)" % (p0,l2fc0,l2fc0)
    if l2fc_se0:
        pf += " and l2fc_se<%f" % l2fc_se0
        
    for x in dbc_fc.find(Q0,F0):
        # Try to keep any probe that passes significance
        Prb += list(pd.DataFrame(x.pop('degs')).query(pf).probe_id.unique())

    Prb = set(Prb)
    X = []
    for x in dbc_fc.find(Q0,F0):
        fc0 = pd.DataFrame(x.pop('degs'))
        fc  = fc0[fc0.probe_id.isin(Prb)].pivot_table(columns='probe_id',values='l2fc')
        for i in x.keys(): fc[i]=x[i]
        X.append(fc.iloc[0].to_dict())
    
    FC = pd.DataFrame(X).set_index(I0).fillna(0)
    if l2fc0:
        N0 = (FC.abs()>l2fc0).sum(axis=0)
        J0 = N0[N0>0].index
        FC = FC[J0]
        
    return FC

def exportFC(chem_name,path,dbc_fc=None,meth='DESeq2'):
    RES = []
    
    for X in dbc_fc.find(dict(name=chem_name,meth=meth),dict(_id=0,trt_grp_cmp_id=0)):
        if not X or not X.has_key('degs'): continue
        FC = pd.DataFrame(X.pop('degs'))
        for i in X.keys():
            FC[i]=X[i]
        RES.append(FC)
    
    RES = pd.concat(RES)
    RES['gene'] = RES.probe_id.str.split('_').apply(lambda i: i[0])
    
    RES.to_csv(path,sep='\t')