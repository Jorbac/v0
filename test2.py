from interpretor import interpretor
from configurer import configurer
from evaluator import evaluator
from admin import admin
from time import time

itp=interpretor('localhost',27017)
config=configurer(itp)
config.ProduceConcreteRule('tenant')
eva=evaluator(itp)






admin=admin(eva,config)




t1=time()

#print eva.concrete_evaluate('orange','Lily','use','vm1')

t2=time()

print t2-t1

for i in range(0,1000):
	eva.concrete_evaluate('orange','Lucy','use','vm5')
t3=time()

print t3-t2



