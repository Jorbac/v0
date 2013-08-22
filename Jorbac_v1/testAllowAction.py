from interpretor import interpretor
from configurer import configurer
from evaluator import evaluator
from admin import admin

itp=interpretor('localhost',27017)
config=configurer(itp)
eva=evaluator(itp)
ad=admin(eva,config)




"""This script performs a complete test of our Python+MongoDB OrBAC single Tenant implementation"""

"""Test Scenario
1. we start from zero having a tenant called "apple"
2. we insert all administrative views including: srole,activity,view,role_assignment,activity_assignment,licence,cross_licence
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



#produce concrete rules
config.ProduceConcreteRule('apple')


"""4. we then use John to create licences for himself for all administrative views, then use John to create different users,actions, resources and assign them to different abstract roles,activities,views"""


#give John the licence to manage role_assignment and role
config.Permission('apple','licence100','apple','admin','manage','role_assignment','nominal')
config.Permission('apple','licence101','apple','admin','manage','role','nominal')
ad.AllowAction('apple','John','insert','apple','role_assignment','John')


config.CreateTenant('null','apple')


