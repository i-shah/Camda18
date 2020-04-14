import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import pandas as pd


def calcStoreFC1(pert_id,dbc_trti=None,dbc_raw=None,dbc_fc=None,):
    K = [u'instance_id',u'scanner', u'name',
         u'gexp_array','cell',
         'pert_id','conc','timeh']

    P = dbc_trti.find_one(dict(pert_id=pert_id))
    P_scans = []
    ScIDs=[P['pert_id']]+P['ctrl_ids']
    
    for X in dbc_raw.find(dict(scan_id={'$in':ScIDs}),
                          dict(_id=0,scan_id=1,probe_levels=1)):
        Y = X.pop('probe_levels')
        X.update(Y)
        X['trt']= 1 if X['scan_id']==P['pert_id'] else 0
        P_scans.append(X)
        
    DF = pd.DataFrame(P_scans).set_index(['trt']).drop('scan_id',axis=1)
    
    X_chem = DF.query("trt==1")
    X_ctrl = DF.query("trt==0").median(axis=0)
    L2FC = X_chem-X_ctrl
    
    Y = {k:P[k] for k in K}
    Y['fc1']=L2FC.iloc[0].to_dict()
    
    if dbc_fc:
        dbc_fc.insert_one(Y)
    else:
        return Y
    
    
def getBounds(X):
    q75, q25 = np.percentile(X.dropna(), [75 ,25])
    iqr = q75 - q25

    return q25 - (iqr*1.5),q75 + (iqr*1.5)

def remOutlier(X):
    IQR = getBounds(X)
    X1 = X[np.logical_or(X<IQR[0],X>IQR[1])]
    return X1

def meanRemOutlier(X):
    return np.mean(remOutlier(X))
    
