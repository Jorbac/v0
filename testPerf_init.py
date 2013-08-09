from interpretor import interpretor
from configurer import configurer
from evaluator import evaluator
from admin import admin
from time import time
from random import random

itp=interpretor('localhost',27017)
config=configurer(itp)
eva=evaluator(itp)
admin=admin(eva,config)


n_role=4
n_activity=4
n_view=4

n_role_subject=10
n_activity_action=10
n_view_object=100

n_abstract_rule=20

n_concrete_rule=n_abstract_rule*n_role_subject*n_activity_action*n_view_object

#drop all collections
itp.cleanAllCollection('test')

"""This script performs a complete test of our Python+MongoDB OrBAC single Tenant implementation"""

"""Test Scenario
1. we start from zero having a tenant called "test"
2. we insert all administrative views including: subject,action,object,role,activity,view,role_assignment,activity_assignment,licence
"""
"""1. we start from zero having a tenant called test"""
#create tenant
config.CreateTenant('null','test')
"""2. we insert all administrative views including: subject,action,object,role,activity,view,role_assignment,activity_assignment,licence
"""
#create administrative views
config.AssignView('null','test',{'_id':'subject','attr':{}})
config.AssignView('null','test',{'_id':'action','attr':{}})
config.AssignView('null','test',{'_id':'object','attr':{}})
config.AssignView('null','test',{'_id':'context','attr':{}})
config.AssignView('null','test',{'_id':'role','attr':{}})
config.AssignView('null','test',{'_id':'activity','attr':{}})
config.AssignView('null','test',{'_id':'view','attr':{}})
config.AssignView('null','test',{'_id':'role_assignment','attr':{}})
config.AssignView('null','test',{'_id':'activity_assignment','attr':{}})
config.AssignView('null','test',{'_id':'licence','attr':{}})
config.AssignView('null','test',{'_id':'cross_licence','attr':{}})


#Assign subject and Role
for i in range(0,n_role):
	config.AssignRole('null','test',{'_id':'role'+str(i),'attr':{}})
	for j in range(0,n_role_subject):
		config.AssignSubject('null','test',{'_id':'subject'+str(i*n_role_subject+j),'attr':{}})
		config.Empower('null','test','subject'+str(i*n_role_subject+j),'role'+str(i))

#Assign action and activity
for i in range(0,n_activity):
	config.AssignActivity('null','test',{'_id':'activity'+str(i),'attr':{}})
	for j in range(0,n_activity_action):
		config.AssignAction('null','test',{'_id':'action'+str(i*n_activity_action+j),'attr':{}})
		config.Consider('null','test','action'+str(i*n_activity_action+j),'activity'+str(i))

#Assign object and view
for i in range(0,n_view):
	config.AssignView('null','test',{'_id':'view'+str(i),'attr':{}})
	for j in range(0,n_view_object):
		config.AssignObject('null','test',{'_id':'object'+str(i*n_view_object+j),'attr':{}})
		config.Use('null','test',{'_id':'object'+str(i*n_view_object+j),'attr':{}},'view'+str(i))
		print 'object'+str(i*n_view_object+j)

#create a context nominal
config.AssignContext('null','test',{'_id':'nominal','attr':{}})


#give licences

m=0

for j in range(0,n_role):
	for k in range(0,n_activity):
		for l in range(0,n_view):
				m=m+1
				print m
				if m<n_abstract_rule:
					config.Permission('null','licence'+str(m),'test','role'+str(j),'activity'+str(k),'view'+str(l),'nominal')
				else:
					exit()


