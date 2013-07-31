from interpretor import interpretor
from configurer import configurer
from evaluator import evaluator
from admin import admin
from time import time

itp=interpretor('localhost',27017)
config=configurer(itp)
eva=evaluator(itp)
admin=admin(eva,config)


"""This script performs a complete test of our Python+MongoDB OrBAC single Tenant implementation"""

"""Test Scenario
1. we start from zero having a tenant called "Orange"
2. we insert all administrative views including: subject,action,object,role,activity,view,role_assignment,activity_assignment,licence
3. we initialize it with assigning "John" to subject, "admin" to role, insert delete to action, insertActivity, deleteActivity and manage to activity and the first licence " John is permitted to manage licence in orange, also "nominal" to context
4. we then use John to create licences for himself for all administrative views, then use John to create different users,actions, resources and assign them to different abstract roles,activities,views
5. use John to assign users privileges
6. use John to assign admin privileges to someone
"""
"""1. we start from zero having a tenant called Orange"""
#create tenant
config.CreateTenant('null','orange')
"""2. we insert all administrative views including: subject,action,object,role,activity,view,role_assignment,activity_assignment,licence
"""
#create administrative views
config.AssignView('null','orange',{'_id':'subject','attr':{}})
config.AssignView('null','orange',{'_id':'action','attr':{}})
config.AssignView('null','orange',{'_id':'object','attr':{}})
config.AssignView('null','orange',{'_id':'context','attr':{}})
config.AssignView('null','orange',{'_id':'role','attr':{}})
config.AssignView('null','orange',{'_id':'activity','attr':{}})
config.AssignView('null','orange',{'_id':'view','attr':{}})
config.AssignView('null','orange',{'_id':'role_assignment','attr':{}})
config.AssignView('null','orange',{'_id':'activity_assignment','attr':{}})
config.AssignView('null','orange',{'_id':'licence','attr':{}})

"""3. we initialize it with assigning "John" to subject, "admin" to role, insert delete to action, insertActivity, deleteActivity and manage to activity and the first licence " John is permitted to manage licence in orange, also "nominal" to context"""
#two default actions: insert and delete, two default activities: insertActivity and deleteActivity, another default activity: manage*
config.AssignAction('null','orange',{'_id':'insert','attr':{}})
config.AssignAction('null','orange',{'_id':'delete','attr':{}})
config.AssignActivity('null','orange',{'_id':'insertActivity','attr':{}})
config.AssignActivity('null','orange',{'_id':'deleteActivity','attr':{}})
config.AssignActivity('null','orange',{'_id':'manage','attr':{}})
config.AssignAction('null','orange',{'_id':'insert','attr':{}})
config.Consider('null','orange','insert','insertActivity')
config.Consider('null','orange','delete','deleteActivity')
config.Consider('null','orange','insert','manage')
config.Consider('null','orange','delete','manage')

#create John, create role admin, assign John to admin
config.AssignSubject('null','orange',{'_id':'John','attr':{}})
config.AssignRole('null','orange',{'_id':'admin','attr':{}})
config.Empower('null','orange','John','admin')

#create a context nominal
config.AssignContext('null','orange',{'_id':'nominal','attr':{}})


#give role admin the first licence to allow it to manage licence
config.Permission('null','licence1','orange','admin','manage','licence','nominal')

"""we now assume the identity of John to perform administrative actions"""

#produce concrete rules
config.ProduceConcreteRule('orange')


"""4. we then use John to create licences for himself for all administrative views, then use John to create different users,actions, resources and assign them to different abstract roles,activities,views"""

#create users
#first we test without the licence to access "subject", we will see that the demand will be rejected
admin.AssignSubject('orange','orange','John',{'_id':'Lily','attr':{}})
#we then use John to create a licence for itself to access view "subject", return "sucess"
admin.Permission('orange','licence2','orange','John','admin','manage','subject','nominal')
#produce concrete rules
config.ProduceConcreteRule('orange')
#we then again insert subject:success
admin.AssignSubject('orange','orange','John',{'_id':'Lily','attr':{}})
admin.AssignSubject('orange','orange','John',{'_id':'Lucy','attr':{}})
admin.AssignSubject('orange','orange','John',{'_id':'Kim','attr':{}})

#we then create two roles dev, s_dev
admin.Permission('orange','licence100','orange','John','admin','manage','role_assignment','nominal')
admin.Permission('orange','licence101','orange','John','admin','manage','role','nominal')
config.ProduceConcreteRule('orange')

#create two roles
admin.AssignRole('orange','orange','John',{'_id':'dev','attr':{}})
admin.AssignRole('orange','orange','John',{'_id':'s_dev','attr':{}})

#role assignment
admin.Empower('orange','orange','John','Lily','dev')
admin.Empower('orange','orange','John','Lucy','dev')
admin.Empower('orange','orange','John','Kim','s_dev')

#we then try insert action use activity useActivity: rejected by AdOrBAC
admin.AssignAction('orange','orange','John',{'_id':'use','attr':{}})
admin.AssignActivity('orange','orange','John',{'_id':'useActivity','attr':{}})
#we then again create a licence for John to enable him to perform such action, and flush the modification

admin.Permission('orange','licence3','orange','John','admin','manage','action','nominal')
admin.Permission('orange','licence4','orange','John','admin','manage','activity','nominal')
admin.Permission('orange','licence5','orange','John','admin','manage','activity_assignment','nominal')
config.ProduceConcreteRule('orange')

#we then try insert action use activity useActivity: succeed
admin.AssignAction('orange','orange','John',{'_id':'use','attr':{}})
admin.AssignActivity('orange','orange','John',{'_id':'useActivity','attr':{}})
admin.Consider('orange','orange','John','use','useActivity')

#then create two groups of resources: normal_vm: vm1 vm2 vm3; critical_vm: vm4 vm5

admin.Permission('orange','licence6','orange','John','admin','manage','object','nominal')
admin.Permission('orange','licence7','orange','John','admin','manage','view','nominal')
config.ProduceConcreteRule('orange')


admin.AssignObject('orange','orange','John',{'_id':'vm1','attr':{}})
admin.AssignObject('orange','orange','John',{'_id':'vm2','attr':{}})
admin.AssignObject('orange','orange','John',{'_id':'vm3','attr':{}})
admin.AssignObject('orange','orange','John',{'_id':'vm4','attr':{}})
admin.AssignObject('orange','orange','John',{'_id':'vm5','attr':{}})
admin.AssignView('orange','orange','John',{'_id':'normalVM','attr':{}})
admin.AssignView('orange','orange','John',{'_id':'criticalVM','attr':{}})
admin.Permission('orange','licence8','orange','John','admin','manage','normalVM','nominal')
admin.Permission('orange','licence9','orange','John','admin','manage','criticalVM','nominal')
config.ProduceConcreteRule('orange')



admin.Use('orange','orange','John',{'_id':'vm1','attr':{}},'normalVM')
admin.Use('orange','orange','John',{'_id':'vm2','attr':{}},'normalVM')
admin.Use('orange','orange','John',{'_id':'vm3','attr':{}},'normalVM')
admin.Use('orange','orange','John',{'_id':'vm4','attr':{}},'criticalVM')
admin.Use('orange','orange','John',{'_id':'vm5','attr':{}},'criticalVM')


"""5. use John to assign users privileges"""
admin.Permission('orange','licence10','orange','John','dev','useActivity','normalVM','nominal')
admin.Permission('orange','licence11','orange','John','s_dev','useActivity','criticalVM','nominal')
config.ProduceConcreteRule('orange')



