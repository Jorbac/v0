from interpretor import interpretor
from configurer import configurer

itp=interpretor('localhost',27017)
config=configurer(itp)
config.AssignSubject('tenant1','tenant',{'_id':'Lily','attr':{}})
