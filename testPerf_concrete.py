
from interpretor import interpretor
from configurer import configurer
from evaluator import evaluator
from admin import admin
from time import time
from random import random

itp=interpretor('localhost',27017)
config=configurer(itp)
eva=evaluator(itp)


t1=time()

#produce concrete rules
config.ProduceConcreteRule('test')

t2=time()

print t2-t1
