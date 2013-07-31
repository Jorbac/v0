from interpretor import interpretor
from configurer import configurer
from evaluator import evaluator
from time import time

itp=interpretor('localhost',27017)
config=configurer(itp)
config.ProduceConcreteRule('tenant')

eva=evaluator(itp)

t1=time()

eva.concrete_evaluate('tenant','John','create','vm1')

t2=time()

print t2-t1

for i in range(0,999):
	eva.concrete_evaluate('tenant','John','create','vm1')
t3=time()

print t3-t2



