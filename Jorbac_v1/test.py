from interpretor import interpretor
from configurer import configurer
from evaluator import evaluator
from admin import admin

itp=interpretor('localhost',27017)
config=configurer(itp)
eva=evaluator(itp)
ad=admin(eva,config)


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

#John try create a permission for himself
ad.Permission('apple','John','test111','apple','admin','manage','role_assignment','nominal')
ad.Permission('apple','John','test113','apple','admin','manage','activity','nominal')
ad.AssignActivity('apple','John',{'_id':'access','attr':{}},'apple')
#consider "read" as "access"
#create some users and resources
config.Consider('apple','read','apple','access')
config.AssignRole('apple',{'_id':'user','attr':{}},'apple')
config.Empower('apple','Alice','apple','user')
config.Use('apple',{'_id':'vm1','attr':{}},'apple','resource')
config.Use('apple',{'_id':'vm2','attr':{}},'apple','resource')
config.Empower('apple','Lily','apple','user')
config.Use('apple',{'_id':'vm3','attr':{}},'apple','resource')
config.Use('apple',{'_id':'vm4','attr':{}},'apple','resource')


ad.Permission('apple','John','test112','apple','admin','manage','role','nominal')
ad.AssignRole('apple','John',{'_id':'dev','attr':{}},'apple')
ad.Empower('apple','John','Alice','apple','dev')

ad.Permission('apple','John','test114','apple','dev','access','resource','nominal')



#create a tenant dep1
config.CreateTenant('apple','dep1')
config.TenantHierarchy('apple','apple','dep1')




"""4. we then use John to create licences for himself for all administrative views, then use John to create different users,actions, resources and assign them to different abstract roles,activities,views"""


#give John the licence to manage role_assignment and role
config.Permission('apple','licence100','apple','admin','manage','role_assignment','nominal')
config.Permission('apple','licence101','apple','admin','manage','role','nominal')

#we then create two roles dev, s_dev,create two roles
config.AssignRole('apple','apple',{'_id':'dev','attr':{}})
config.AssignRole('apple','apple',{'_id':'s_dev','attr':{}})

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



ad.AllowAction('apple','John','insert','apple','role_assignment','John')


