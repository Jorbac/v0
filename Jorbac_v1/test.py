from interpretor import interpretor
from configurer import configurer
from evaluator import evaluator
from admin import admin

itp=interpretor('localhost',27017)
config=configurer(itp)
eva=evaluator(itp)
ad=admin(eva,config)

ad.AllowAction('apple','John','insert','apple','role_assignment','John')


"""This script performs a complete test of our Python+MongoDB OrBAC single Tenant implementation"""

"""Test Scenario
1. we start from zero having a tenant called "apple"
2. we insert all administrative views including: subject,action,object,role,activity,view,role_assignment,activity_assignment,licence
3. we initialize it with assigning "John" to subject, "admin" to role, insert delete to action, insertActivity, deleteActivity and manage to activity and the first licence " John is permitted to manage licence in apple, also "nominal" to context
4. we then use John to create licences for himself for all administrative views, then use John to create different users,actions, resources and assign them to different abstract roles,activities,views
5. use John to assign users privileges
6. use John to assign admin privileges to someone
"""
"""1. we start from zero having a tenant called apple"""
#create tenant
config.CreateTenant('null','apple')
"""2. we insert all administrative views including: subject,action,object,role,activity,view,role_assignment,activity_assignment,licence
"""
#create administrative views
config.AssignView('null','apple',{'_id':'subject','attr':{}})
config.AssignView('null','apple',{'_id':'action','attr':{}})
config.AssignView('null','apple',{'_id':'object','attr':{}})
config.AssignView('null','apple',{'_id':'context','attr':{}})
config.AssignView('null','apple',{'_id':'role','attr':{}})
config.AssignView('null','apple',{'_id':'activity','attr':{}})
config.AssignView('null','apple',{'_id':'view','attr':{}})
config.AssignView('null','apple',{'_id':'role_assignment','attr':{}})
config.AssignView('null','apple',{'_id':'activity_assignment','attr':{}})
config.AssignView('null','apple',{'_id':'licence','attr':{}})
config.AssignView('null','apple',{'_id':'cross_licence','attr':{}})

"""3. we initialize it with assigning "John" to subject, "admin" to role, insert delete to action, insertActivity, deleteActivity and manage to activity and the first licence " John is permitted to manage licence in apple, also "nominal" to context"""
#two default actions: insert and delete, two default activities: insertActivity and deleteActivity, another default activity: manage*
config.AssignActivity('null','apple',{'_id':'insertActivity','attr':{}})
config.AssignActivity('null','apple',{'_id':'deleteActivity','attr':{}})
config.AssignActivity('null','apple',{'_id':'manage','attr':{}})

config.Consider('null','insert','apple','insertActivity')
config.Consider('null','delete','apple','deleteActivity')
config.Consider('null','insert','apple','manage')
config.Consider('null','delete','apple','manage')

#create John, create role admin, assign John to admin
config.AssignRole('null','apple',{'_id':'admin','attr':{}})
config.Empower('null','John','apple','admin')

#create a context nominal
config.AssignContext('null','apple',{'_id':'nominal','attr':{}})


#give role admin the first licence to allow it to manage licence
config.Permission('null','licence1','apple','admin','manage','licence','nominal')

"""we now assume the identity of John to perform administrative actions"""

#produce concrete rules
config.ProduceConcreteRule('apple')


"""4. we then use John to create licences for himself for all administrative views, then use John to create different users,actions, resources and assign them to different abstract roles,activities,views"""

#create users
#first we test without the licence to create "subject", we will see that the demand will be rejected
admin.AssignSubject('apple','apple','John',{'_id':'Lily','attr':{}})
#we then use John to create a licence for itself to access view "subject", return "sucess"
admin.Permission('apple','licence2','apple','John','admin','manage','subject','nominal')
#produce concrete rules
config.ProduceConcreteRule('apple')
#we then again insert subject:success
admin.AssignSubject('apple','apple','John',{'_id':'Lily','attr':{}})
admin.AssignSubject('apple','apple','John',{'_id':'Lucy','attr':{}})
admin.AssignSubject('apple','apple','John',{'_id':'Kim','attr':{}})

#give John the licence to manage role_assignment and role
admin.Permission('apple','licence100','apple','John','admin','manage','role_assignment','nominal')
admin.Permission('apple','licence101','apple','John','admin','manage','role','nominal')
config.ProduceConcreteRule('apple')

#we then create two roles dev, s_dev,create two roles
admin.AssignRole('apple','apple','John',{'_id':'dev','attr':{}})
admin.AssignRole('apple','apple','John',{'_id':'s_dev','attr':{}})

#role assignment
admin.Empower('apple','apple','John','Lily','dev')
admin.Empower('apple','apple','John','Lucy','dev')
admin.Empower('apple','apple','John','Kim','s_dev')

#we then try insert action use activity useActivity: rejected by AdOrBAC
admin.AssignAction('apple','apple','John',{'_id':'use','attr':{}})
admin.AssignActivity('apple','apple','John',{'_id':'useActivity','attr':{}})
#we then again create a licence for John to enable him to perform such action, and flush the modification

admin.Permission('apple','licence3','apple','John','admin','manage','action','nominal')
admin.Permission('apple','licence4','apple','John','admin','manage','activity','nominal')
admin.Permission('apple','licence5','apple','John','admin','manage','activity_assignment','nominal')
config.ProduceConcreteRule('apple')

#we then try insert action use activity useActivity: succeed
admin.AssignAction('apple','apple','John',{'_id':'use','attr':{}})
admin.AssignActivity('apple','apple','John',{'_id':'useActivity','attr':{}})
admin.Consider('apple','apple','John','use','useActivity')

#then create two groups of resources: normal_vm: vm1 vm2 vm3; critical_vm: vm4 vm5

admin.Permission('apple','licence6','apple','John','admin','manage','object','nominal')
admin.Permission('apple','licence7','apple','John','admin','manage','view','nominal')
config.ProduceConcreteRule('apple')


admin.AssignObject('apple','apple','John',{'_id':'vm1','attr':{}})
admin.AssignObject('apple','apple','John',{'_id':'vm2','attr':{}})
admin.AssignObject('apple','apple','John',{'_id':'vm3','attr':{}})
admin.AssignObject('apple','apple','John',{'_id':'vm4','attr':{}})
admin.AssignObject('apple','apple','John',{'_id':'vm5','attr':{}})
admin.AssignView('apple','apple','John',{'_id':'normalVM','attr':{}})
admin.AssignView('apple','apple','John',{'_id':'criticalVM','attr':{}})
admin.Permission('apple','licence8','apple','John','admin','manage','normalVM','nominal')
admin.Permission('apple','licence9','apple','John','admin','manage','criticalVM','nominal')
config.ProduceConcreteRule('apple')



admin.Use('apple','apple','John',{'_id':'vm1','attr':{}},'normalVM')
admin.Use('apple','apple','John',{'_id':'vm2','attr':{}},'normalVM')
admin.Use('apple','apple','John',{'_id':'vm3','attr':{}},'normalVM')
admin.Use('apple','apple','John',{'_id':'vm4','attr':{}},'criticalVM')
admin.Use('apple','apple','John',{'_id':'vm5','attr':{}},'criticalVM')


"""5. use John to assign users privileges"""
admin.Permission('apple','licence10','apple','John','dev','useActivity','normalVM','nominal')
admin.Permission('apple','licence11','apple','John','s_dev','useActivity','criticalVM','nominal')
config.ProduceConcreteRule('apple')



