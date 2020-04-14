import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri

loadAffyCels = robjects.r("""
library(affy)
loadAffyCels <- function(d,o){
    setwd(d)
    c1 <- ReadAffy()
    e1 <- rma(c1)
    write.exprs(e1,file=o)
}
""")

R_loadAffyCelsFiles = robjects.r("""
library(affy)
loadAffyCelsFiles <- function(f,d){
    setwd(d)
    c1 <- ReadAffy(filenames=f)
    e1 <- rma(c1)
    p1 <- pData(e1)
    d1 <- exprs(e1)
    cbind(p1,t(d1))
}
""")

def loadAffyCelsNorm(F,d):
    F1 = robjects.vectors.StrVector(F)
    #F1 = 'c('+ ','.join(["'%s'"%i for i in F])+')'
    E1 = R_loadAffyCelsFiles(F1,d)
    X1 = pandas2ri.ri2py_dataframe(E1)
    X1['cel']=F
    return X1

R_getAffyCel = robjects.r("""
library(affyio)    
getAffyCel <- function(cel){
    H <- read.celfile.header(cel)
    H
}
""")

def getAffyCelCdf(cel):
    y = R_getAffyCel(cel)
    return pandas2ri.ri2py_listvector(y)[0][0]

