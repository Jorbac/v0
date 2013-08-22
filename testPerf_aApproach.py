from interpretor import interpretor
from configurer import configurer
from evaluator import evaluator
from time import time
import random




itp=interpretor('localhost',27017)
config=configurer(itp)


eva=evaluator(itp)

s_n=random.randrange(0,100)
a_n=random.randrange(0,100)
o_n=random.randrange(0,4000)

t1=time()

eva.abstract_evaluate('test','subject'+str(s_n),'action'+str(a_n),'object'+str(o_n))

t2=time()

print t2-t1


for i in range(0,50):
	s_n=random.randrange(0,100)
	a_n=random.randrange(0,100)
	o_n=random.randrange(0,4000)
	eva.abstract_evaluate('test','subject'+str(s_n),'action'+str(a_n),'object'+str(o_n))
t3=time()

print t3-t2

