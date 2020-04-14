import pymongo
import os

def openMongo(host="pb.epa.gov",user=None,passwd=None,db=None):
    if not user or passwd:
        user,passwd = file(os.getenv('HOME')+'/.mngdb/passwd').read().strip().split(':')
        
    con2 = pymongo.MongoClient("mongodb://%s:%s@%s/%s" % (user,passwd,host,db))
    DB = con2[db]
    return DB